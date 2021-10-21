# -*- coding: utf-8 -*-

# !!! try implementing a general getter, a general processor, a general checker, a general pipeline
# and extend them using design pattern

from pdfminer.high_level import extract_text
import re
import os
import glob
from datetime import datetime

YEAR = datetime.now().year
SRC_FOLDER = 'C:\\Users\\Tales\\Desktop\\graviola\\src'
SRC_FOLDER = os.path.dirname(__file__)
GRAV_FOLDER = os.path.dirname(SRC_FOLDER)
APS_FOLDER = GRAV_FOLDER + os.sep + 'aps'
STATES = ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE',
          'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO')
OUTPUT_FOLDER = GRAV_FOLDER + os.sep + 'output'
OUTPUT_CSV_FILE = OUTPUT_FOLDER + os.sep + 'output.csv'

#==================================================================================================
# HELPER FUNCTIONS

def get_text_between(this, that):
    compiled_regex = re.compile(f'{this}(.*?){that}', re.VERBOSE)
    return compiled_regex

def get_pdf_files():
    pdf_files = [pdf for pdf in glob.glob(APS_FOLDER + os.sep + '*.pdf')]
    return pdf_files

def build_ap(string):
    ap_num = ApProcessor().pipeline_ap(string)
    value = ValueProcessor().pipeline_value(string)
    cpf, account_num = CPFAndAccountProcessor().pipeline_cpf_and_account(string)
    process_num = ProcessNumProcessor().pipeline_process_num(string)
    branch_num = BranchProcessor().pipeline_branch_num(string)
    ne_num = NeProcessor().pipeline_ne(string)
    subelement_num = SubelementProcessor().pipeline_subelement(string)
    observation = ObservationProcessor().pipeline_observation(string)
    
    return Ap(ap_num, value, cpf, account_num, process_num, branch_num, ne_num, 
              subelement_num, observation)

#==================================================================================================

class FromPdfToString():
    def __init__(self, pdf_filepath):
        self.pdf_filepath = pdf_filepath
        self.string = self.process_input(self.pdf_filepath)
    
    def get_raw_string(self, pdf_filepath):
        raw_string = extract_text(pdf_filepath)
        return raw_string
        
    def eliminate_newlines(self, string):
        string_no_newlines = string.replace('\n', ' ')
        return string_no_newlines
        
    def eliminate_multiple_spaces(self, string):
        string_no_spaces = ' '.join(string.split())
        return string_no_spaces
    
    def process_input(self, pdf_filepath):
        raw_string = self.get_raw_string(pdf_filepath)
        string_no_newlines = self.eliminate_newlines(raw_string)
        string_no_spaces = self.eliminate_multiple_spaces(string_no_newlines)
        return string_no_spaces
    
    def get_string(self):
        return self.string
        
class Ap():
    def __init__(self, ap_num, value, cpf, account_num, process_num, branch_num,
                 ne_num, subelement_num, observation):
        self.ap_num = ap_num
        self.value = value
        self.cpf = cpf
        self.account_num = account_num
        self.process_num = process_num
        self.branch_num = branch_num
        self.ne_num = ne_num
        self.subelement_num = subelement_num
        self.observation = observation
        
    def ap_as_tuple(self):
        return (self.ap_num,
                self.value,
                self.cpf,
                self.account_num, 
                self.process_num, 
                self.branch_num,
                self.ne_num,
                self.subelement_num,
                self.observation)
        
    def to_scsv(self):
        one_line = ';'.join(self.ap_as_tuple())
        
        with open(OUTPUT_CSV_FILE, 'a', encoding = 'utf-8') as f:
            f.write(one_line + '\n')

class ValueProcessor():        
    def _get_value(self, string):
        pattern = get_text_between('IMPORTÂNCIA\sA\sPAGAR:\sR\$', '\(')
        match = re.search(pattern, string)
        raw_value = match.groups()[0]
        return raw_value
        
    def _strip_raw_value(self, raw_value):
        return raw_value.strip()
    
    def _is_valid(self, stripped_value):
        pattern = '.*\d,\d\d$' # 0,00 15,95 1.396,37
        match = re.search(pattern, stripped_value)
        
        return (match is not None)
    
    def pipeline_value(self, string):
        try: 
            raw_value = self._get_value(string)
            stripped_value = self._strip_raw_value(raw_value)
            
            if self._is_valid(stripped_value):
                return stripped_value
            else:
                raise ValueError(f'Failed to recognize input value. Got {stripped_value}')
        except Exception as e:
            print(e)
            return 'NA'

# !!! not a good solution. CPF may appear away from vencimento

class CPFAndAccountProcessor():
    def _get_cpf_and_account(self, string):
        pattern = r'''DATA:\s\d{2}/\d{2}/\d{4}\s         # started by DATA: 01/01/2021
                              CPF\s(\d{3}\.\d{3}\.\d{3}-\d{2})   # CPF 333.333.333.33
                              (.*)                               # account_number
                              (?=\sVENCIMENTO)'''                # always followed by ' VENCIMENTO'
        match = re.search(pattern, string, re.VERBOSE)
        raw_cpf_and_account = match.groups()[:2]
        
        return raw_cpf_and_account
    # def _get_cpf_and_account(self, string):
    #     pattern = get_text_between('CPF', 'VENCIMENTO')
    #     match = re.search(pattern, string)
    #     raw_cpf_and_account = match.groups()[0]
    #     return raw_cpf_and_account

    def _separate_cpf_and_account(self, raw_cpf_and_account):
        return (raw_cpf_and_account[0], raw_cpf_and_account[1])
    
    def _is_cpf_valid(self, cpf):
        pattern = '^\d{3}\.\d{3}\.\d{3}-\d{2}$' # e.g. 000.000.000-00
        match = re.search(pattern, cpf)
        
        return (match is not None)
    
    def _is_account_valid(self, account):
        pattern = '[^\d.xX-]' # gets anything that is not a number, dot, the letter x or hyphen
        match = re.search(pattern, account) # to be valid, this has to be empty
        
        return (match is None)
    
    def pipeline_cpf_and_account(self, string):
        try:
            raw_cpf_and_account = self._get_cpf_and_account(string)
            cpf, account = self._separate_cpf_and_account(raw_cpf_and_account)
            
            cpf = cpf.strip()
            account = account.strip()
            
            if self._is_cpf_valid(cpf):
                pass
            else:
                raise ValueError(f'Failed to recognize input CPF. Got {cpf}')
                
            if self._is_account_valid(account):
                pass
            else:
                raise ValueError(f'Failed to recognize input account number. Got {account}')
            
            return (cpf, account)
            
        except Exception as e:
            print(e)
            return ('NA', 'NA')

class NeProcessor():
    def _get_ne(self, string):
        pattern = get_text_between('EMPENHO', 'ELEM.\sDE\sDESPESA')
        match = re.search(pattern, string)
        raw_ne = match.groups()[0]
        return raw_ne
    
    def _strip_raw_ne(self, raw_ne):
        return raw_ne.strip()
    
    def _is_ne_valid(self, stripped_ne):
        pattern = r'\d{4}NE\d{6}'
        match = re.search(pattern, stripped_ne)
        
        return (match is not None)
    
    def pipeline_ne(self, string):
        try: 
            raw_ne = self._get_ne(string)
            stripped_ne = self._strip_raw_ne(raw_ne)
            
            if self._is_ne_valid(stripped_ne):
                return stripped_ne
            else:
                raise ValueError(f'Failed to recognize input NE number. Got {stripped_ne}')
        except Exception as e:
            print(e)
            return 'NA'
        
class ApProcessor():
    def _get_ap(self, string):
        pattern = r'''AP\snº\s(\d{1,3}/\d{4})''' # AP nº 350/2021
        match = re.search(pattern, string, re.VERBOSE)
        raw_ap = match.groups()[0]
        return raw_ap
    
    # def _get_ap(self, string):
    #     pattern = get_text_between('AP\snº', 'AUTORIZAÇÃO')
    #     match = re.search(pattern, string)
    #     raw_ap = match.groups()[0]
    #     return raw_ap
    
    def _strip_raw_ap(self, raw_ap):
        return raw_ap.strip()
    
    def _is_ap_valid(self, stripped_ap):
        pattern = '\d{1,3}/\d{4}'
        match = re.search(pattern, stripped_ap)
        
        return (match is not None)
    
    def pipeline_ap(self, string):
        try:
            raw_ap = self._get_ap(string)
            stripped_ap = self._strip_raw_ap(raw_ap)
        
            if self._is_ap_valid(stripped_ap):
                return stripped_ap
            else:
                raise ValueError(f'Failed to recognize input AP number. Got {stripped_ap}')
        except Exception as e:
            print(e)
            return 'NA'

class ProcessNumProcessor():
    def _get_process_num(self, string):
        pattern = get_text_between('EXPEDIENTE', 'FAVORECIDO')
        match = re.search(pattern, string)
        raw_process_num = match.groups()[0]
        return raw_process_num
    
    def _strip_process_num(self, raw_process_num):
        return raw_process_num.strip()
    
    def _is_process_num_valid(self, stripped_process_num):
        pattern = '\d{7}\.\d{8}/\d{4}-\d{2}'
        match = re.search(pattern, stripped_process_num)
        
        return (match is not None)
    
    def pipeline_process_num(self, string):
        try:
            raw_process_num = self._get_process_num(string)
            stripped_process_num = self._strip_process_num(raw_process_num)
            
            if self._is_process_num_valid(stripped_process_num):
                return stripped_process_num
            else:
                raise ValueError(f'Failed to recognize input process number. Got {stripped_process_num}')
        except Exception as e:
            print(e)
            return 'NA'
            
class BranchProcessor():
    def _get_branch_num(self, string):
        pattern = r'''\s
                      \d{1,5}(-\d)?       # 1, 2, 3, 4 or 5 digits. Sometimes followed by hyphen and a confirmation digit 
                      (?=\sHISTÓRICO)'''  # always followed by HISTÓRICO
        match = re.search(pattern, string, re.VERBOSE)
        raw_branch_num = match.group()
        
        return raw_branch_num
    
    def _strip_branch_num(self, raw_branch_num):
        return raw_branch_num.strip()
    
    def _remove_dash_from_branch_num(self, stripped_branch_num):
        index = stripped_branch_num.find('-')
        if index == -1:
            return stripped_branch_num
        else:
            return stripped_branch_num[:index] # removes the hyphen with everything that comes after it
        
    def _reduce_to_only_4_digits(self, branch_num_no_dashes):
        if len(branch_num_no_dashes) > 4:
            return branch_num_no_dashes[1:5]
        else:
            return branch_num_no_dashes
    
    def _is_branch_num_valid(self, branch_num):        
        pattern = '\d{1,4}'
        match = re.search(pattern, branch_num)
        
        return (match is not None)
    
    def pipeline_branch_num(self, string):
        try:
            raw_branch_num = self._get_branch_num(string)
            stripped_branch_num = self._strip_branch_num(raw_branch_num)
            branch_num_no_dashes = self._remove_dash_from_branch_num(stripped_branch_num)
            branch_num_4_digits = self._reduce_to_only_4_digits(branch_num_no_dashes)
        
            if self._is_branch_num_valid(branch_num_4_digits):
                return branch_num_4_digits
            else:
                raise ValueError(f'Failed to recognize input process number. Got {branch_num_4_digits}')
                
        except Exception as e:
            print(e)
            return 'NA'
    
class SubelementProcessor():
    def _get_subelement(self, string):
        pattern = get_text_between('ELEM\.\sDE\sDESPESA', 'ITEM\sDE\sPROG')
        match = re.search(pattern, string)
        raw_subelement = match.groups()[0]
        return raw_subelement
    
    def _strip_subelement(self, raw_subelement):
        return raw_subelement.strip()
    
    def _is_subelement_valid(self, stripped_subelement):
        pattern = r'\d{4}\.\d{2}-\d{2}'
        match = re.search(pattern, stripped_subelement)
        
        return (match is not None)
    
    def pipeline_subelement(self, string):
        try:
            raw_subelement = self._get_subelement(string)
            stripped_subelement = self._strip_subelement(raw_subelement)
            
            if self._is_subelement_valid(stripped_subelement):
                return stripped_subelement
            else:
                raise ValueError(f'Failed to recognize input subelement number. Got {stripped_subelement}')
            
        except Exception as e:
            print(e)
            pass
        
class ObservationProcessor():
    def _get_observation(self, string):
        # gets everything that comes after HISTÓRICO and ends in '- AA', where AA are both capital letters
        pattern = r'HISTÓRICO(.*?-\s[A-Z][A-Z])'
        match = re.search(pattern, string)
        raw_observation = match.groups()[0]
        return raw_observation                               
    
    def _strip_observation(self, raw_observation):
        return raw_observation.strip()
    
    def _is_observation_valid(self, stripped_observation):
        if stripped_observation[-2:] not in STATES:
            return False
        if len(stripped_observation) > 500:
            return False
        
        return True
    
    def pipeline_observation(self, string):
        try:
            raw_observation = self._get_observation(string)
            stripped_observation = self._strip_observation(raw_observation)
        
            if self._is_observation_valid(stripped_observation):
                return stripped_observation
            else:
                raise ValueError(f'Failed to recognize input observation text. Got {stripped_observation}')
        except Exception as e:
            print(e)
            return 'NA'    

if __name__ == '__main__':
    os.chdir(APS_FOLDER)
    pdf_files = get_pdf_files()
    
    for i in range(len(pdf_files)):
        string = extract_text(pdf_files[i])
        with open(f'{i}.txt', 'w') as f:
            f.write(string)
    
    # string = extract_text(pdf_file)
    # with open('bug.txt', 'w') as f:
    #     f.write(string)
        
    # string = FromPdfToString(pdf_file).get_string()
    # ap = build_ap(string)
    
    # with open('bug.txt', 'w') as f:
    #     f.write(string)
        
    # c = CPFAndAccountProcessor()
    # s = c._get_cpf_and_account(string)
    
    
    # for pdf_file in pdf_files:
    #     string = FromPdfToString(pdf_file).get_string()
    #     ap = build_ap(string)
    #     ap.to_scsv()
        


