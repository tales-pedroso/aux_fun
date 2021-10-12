# -*- coding: utf-8 -*-
from pdfminer.high_level import extract_text
import re
import os
import glob

# finish getting the encoding right

#SRC_FOLDER = 'C:\\Users\\Tales\\Desktop\\graviola\\src'
SRC_FOLDER = os.path.dirname(__file__)
GRAV_FOLDER = os.path.dirname(SRC_FOLDER)
APS_FOLDER = GRAV_FOLDER + os.sep + 'aps'
STATES = ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE',
          'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO')
OUTPUT_FOLDER = GRAV_FOLDER + os.sep + 'output'
OUTPUT_CSV_FILE = OUTPUT_FOLDER + os.sep + 'output.csv'

def get_pdf_files():
    pdf_files = [pdf for pdf in glob.glob(APS_FOLDER + os.sep + '*.pdf')]
    return pdf_files

value_regex = re.compile(r'''IMPORTÂNCIA      # gets everything after R$
                             .*               # and before )
                             R\$              # e.g. IMPORTÂNCIA A PAGAR: R$ 6.661,57 (seis mil ...)
                             (.*\d\d.*)       # returns ' 6.661,57 '
                             \(               #
                          ''', re.VERBOSE)

cpf_and_account_num_regex = re.compile(r'''CPF                           # gets the cpf number
                                           .*                            # after 'CPF' and it gets the account number
                                           (\d{3}\.\d{3}\.\d{3}-\d{2})   # that comes after the CPF number
                                           (.*)                          # and before 'VENCIMENTO'
                                           VENCIMENTO                    # e.g. CPF 539.170.227-53 48062-9 VENCIMENTO
                                        ''', re.VERBOSE)                 # returns '539.170.227-53' and ' 48062-9 '

ap_num_regex = re.compile(r'''AP\snº\s         # gets the number and date after 'AP nº '
                              (\d{1,3}/\d{4})  # e.g. AP nº 372/2021
                          ''', re.VERBOSE)     # returns '372/2021'

process_num_regex = re.compile(r'''EXPEDIENTE            # gets everything between 'EXPEDIENTE''
                                   (.*)                  # and 'FAVORECIDO'
                                   FAVORECIDO            # e.g. Nº DO PROC/EXPEDIENTE 0045142.00001072/2021-87 FAVORECIDO
                                ''', re.VERBOSE)         # returns ' 0045142.00001072/2021-87 '

branch_num_regex = re.compile(r'''(\d{2,4})        # gets the number that comes before 'HISTÓRICO''
                                  .*               # e.g. 12 123 12-3 1234 123-4 12345 1234-5 
                                  HISTÓRICO        # returns '12' '123' '12' '1234' '123' '1234' '1234'
                              ''', re.VERBOSE)
                              
ne_num_regex = re.compile(r'''EMPENHO              # gets the number between 'EMPENHO'
                              (.*)                 # and 'ELEM. DE DESPESA'
                              ELEM.
                          ''', re.VERBOSE)

subelement_num_regex = re.compile(r'''ELEM\.\sDE\sDESPESA
                                  (.*)
                                  ITEM\sDE\sPROG
                                  ''', re.VERBOSE)

observation_regex = re.compile(r'''HISTÓRICO       # gets everything that comes after HISTÓRICO
                               (.*?-\s[A-Z][A-Z])   # and it ends in "- AA", where A is any capital letter                               
                               ''', re.VERBOSE)    # HISTÓRICO Autorizo pagamento (...) Rio de Janeiro - RJ

# def get_value(string):
#     '''
#     multiple values appear throughout the document. the one that matters is
#     always preceded by 'IMPORTÂNCIA A PAGAR: R$' and it always end before a 
#     closing parentheses
#     e.g. IMPORTÂNCIA A PAGAR: R$ 6.661,57 (
#     '''
#     match = re.search(value_regex, string)
#     value = match.groups()[0].strip()
#     return value

# def get_cpf_and_account_num(string):
#     '''
#     multiple cpf values appear throughout the document. the one that matters
#     comes right before the account number, which comes right before the 
#     word 'VENCIMENTO'
#     e.g. CPF 539.170.227-53 48062-9 VENCIMENTO
#     '''
#     match = re.search(cpf_and_account_num_regex, string)
#     cpf = match.groups()[0]
#     account_num = match.groups()[1].strip()
#     return dict(cpf = cpf, account_num = account_num)

# def get_ap_num(string):
#     '''
#     multiple numbers appear throught the document. the one that matters comes
#     right after "AP nº" and it is a sequence of at most 3 digits, followed by
#     a date with 4 digits
#     e.g. AP nº 372/2021
#     '''
#     match = re.search(ap_num_regex, string)
#     ap_num = match.groups()[0].strip()
#     return ap_num

# def get_process_num(string):
#     '''
#     multiple numbers appear throught the document. the one that matters comes
#     right after "EXPEDIENTE" and right before "FAVORECIDO"
#     e.g. Nº DO PROC/EXPEDIENTE 0045142.00001072/2021-87 FAVORECIDO
#     '''
#     match = re.search(process_num_regex, string)
#     process_num = match.groups()[0].strip()
#     return process_num

# def get_branch_num(string):
#     '''
#     gets the numbers that come before "HISTÓRICO". it does not take the 
#     confirmation code that comes after '-'. returns a 4-digit number, filling
#     the left-hand side with zeros, when needed
#     e.g. 12 -> '0012' 12-3 -> '0012'
#     '''
#     match = re.search(branch_num_regex, string)
#     branch_num = match.groups()[0]
#     branch_num = branch_num.zfill(4)
#     return branch_num
    
# def get_ne_num(string):
#     '''
#     '''
#     match = re.search(ne_num_regex, string)
#     ne_num = match.groups()[0].strip()
#     return ne_num
    
# def get_subelement_num(string):
#     match = re.search(subelement_num_regex, string)
#     subelement_num = match.groups()[0].strip()
#     return subelement_num

# def get_observation(string):
#     match = re.search(observation_regex, string)
#     observation = match.groups()[0].strip()
    
#     if observation[-2:] not in STATES:
#         raise Exception(f'''Falha em extrair a observação da AP. Esperava um texto terminado em sigla
#                         de um Estado, e.g. RJ, SP, PE. Encontrou: {match.groups()[0]}''')
#     else: 
#         return observation

class FromPdfToString(object):
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
        
class AP(object):
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
    
class FromStringToAP(object):
    def __init__(self, string):
        self.string = string
        self.get_value(self.string)
        self.get_cpf_and_account_num(self.string)
        self.get_ap_num(self.string)
        self.get_process_num(self.string)
        self.get_branch_num(self.string)
        self.get_ne_num(self.string)
        self.get_subelement_num(self.string) 
        self.get_observation(self.string)
        self.to_ap()
        
    def get_value(self, string):
        '''
        multiple values appear throughout the document. the one that matters is
        always preceded by 'IMPORTÂNCIA A PAGAR: R$' and it always end before a 
        closing parentheses
        e.g. IMPORTÂNCIA A PAGAR: R$ 6.661,57 (
        '''
        match = re.search(value_regex, string)
        value = match.groups()[0].strip()
        self.value = value

    def get_cpf_and_account_num(self, string):
        '''
        multiple cpf values appear throughout the document. the one that matters
        comes right before the account number, which comes right before the 
        word 'VENCIMENTO'
        e.g. CPF 539.170.227-53 48062-9 VENCIMENTO
        '''
        match = re.search(cpf_and_account_num_regex, string)
        cpf = match.groups()[0]
        account_num = match.groups()[1].strip()
        self.cpf = cpf
        self.account_num = account_num

    def get_ap_num(self, string):
        '''
        multiple numbers appear throught the document. the one that matters comes
        right after "AP nº" and it is a sequence of at most 3 digits, followed by
        a date with 4 digits
        e.g. AP nº 372/2021
        '''
        match = re.search(ap_num_regex, string)
        ap_num = match.groups()[0].strip()
        self.ap_num = ap_num

    def get_process_num(self, string):
        '''
        multiple numbers appear throught the document. the one that matters comes
        right after "EXPEDIENTE" and right before "FAVORECIDO"
        e.g. Nº DO PROC/EXPEDIENTE 0045142.00001072/2021-87 FAVORECIDO
        '''
        match = re.search(process_num_regex, string)
        process_num = match.groups()[0].strip()
        self.process_num = process_num

    def get_branch_num(self, string):
        '''
        gets the numbers that come before "HISTÓRICO". it does not take the 
        confirmation code that comes after '-'. returns a 4-digit number, filling
        the left-hand side with zeros, when needed
        e.g. 12 -> '0012' 12-3 -> '0012'
        '''
        match = re.search(branch_num_regex, string)
        branch_num = match.groups()[0]
        branch_num = branch_num.zfill(4)
        self.branch_num = branch_num
    
    def get_ne_num(self, string):
        match = re.search(ne_num_regex, string)
        ne_num = match.groups()[0].strip()
        self.ne_num = ne_num
    
    def get_subelement_num(self, string):
        match = re.search(subelement_num_regex, string)
        subelement_num = match.groups()[0].strip()
        self.subelement_num = subelement_num

    def get_observation(self, string):
        match = re.search(observation_regex, string)
        observation = match.groups()[0].strip()
    
        if observation[-2:] not in STATES:
            raise Exception(f'''Falha em extrair a observação da AP. Esperava um texto terminado em sigla
                            de um Estado, e.g. RJ, SP, PE. Encontrou: {match.groups()[0]}''')
        else: 
            self.observation = observation
    
    def to_ap(self):
        ap = AP(ap_num = self.ap_num,
                value = self.value, 
                cpf = self.cpf,
                account_num = self.account_num,
                process_num = self.process_num, 
                branch_num = self.branch_num,
                ne_num = self.ne_num,
                subelement_num = self.subelement_num,
                observation = self.observation)
        self.ap = ap
        
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
        '''
        semi-colon separated value
        '''
        one_line = ';'.join(self.ap_as_tuple())
        
        with open(OUTPUT_CSV_FILE, 'a', encoding = 'utf-8') as f:
            f.write(one_line + '\n')

if __name__ == '__main__':
    os.chdir(APS_FOLDER)
    pdf_files = get_pdf_files()
    
    for pdf_file in pdf_files:
        string = FromPdfToString(pdf_file).get_string()
        ap = FromStringToAP(string)
        ap.to_scsv()
        


