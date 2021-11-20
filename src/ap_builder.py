# -*- coding: utf-8 -*-
# those classes could be just regular dicts or some extension of them
# insert validation of values later, e.g. cpf validation

from datetime import date
import pipeline

def today():
    format_ = "%d/%m/%Y"
    today = date.today()
    formatted_today = today.strftime(format_)
    return formatted_today

def create_observation(deceased_person_name, date_of_death, ap_num, process_num):
    observation = f'Pagamento do auxílio-funeral de {deceased_person_name}, falecido/a em {date_of_death}. AP {ap_num}. Processo: {process_num}.'
    return observation

class AuxFunBasicData():
    def __init__(self, process_num, value, cpf, ap_date, ap_num, date_of_death, deceased_person_name):
        self.process_num = process_num
        self.set_truncated_process_num()
        self.value = value
        self.cpf = cpf
        self.set_cpf_just_numbers()
        self.ap_date = ap_date
        self.ap_num = ap_num
        self.date_of_death = date_of_death
        self.deceased_person_name = deceased_person_name
        
        self.set_due_date()
        self.set_observation()
        
    def set_truncated_process_num(self):
        first_part = self.process_num[2:8]  # 0045142.  -> 45142. 
        second_part = self.process_num[10:] # 00001057/2021-65 -> 001057/2021-65
        truncated = first_part + second_part
        self.truncated_process_num = truncated
        
    def set_cpf_just_numbers(self):
        no_dots = self.cpf.replace('.', '')
        no_dashes = no_dots.replace('-', '')
        self.cpf_just_numbers = no_dashes
        
    def set_due_date(self):
        self.due_date = today()
        
    def set_observation(self):
        self.observation = create_observation(self.deceased_person_name, 
                                              self.date_of_death, self.ap_num, 
                                              self.process_num)
        
    def to_dict(self):
        output_dict = dict(due_date = self.due_date, 
                           process_num = self.process_num,
                           truncated_process_num = self.truncated_process_num,
                           validation_date = self.ap_date,
                           value = self.value,
                           recipient = self.cpf_just_numbers,
                           observation = self.observation)
        return output_dict
            
class AuxFunSourceDoc():
    def __init__(self, ap_num, value, ap_date):
        self.ap_num = f'AP {ap_num}'       
        self.value = value
        self.ap_date = ap_date
        
        self.set_emitter()
        
    def set_emitter(self):
        self.doc_emitter = '114601'
    
    def to_dict(self):
        output_dict = dict(doc_emitter = self.doc_emitter,
                           ap_date = self.ap_date,
                           ap_num = self.ap_num,
                           value = self.value)
        return output_dict
    
class AuxFunPco():
    def __init__(self, ne_num, subelement_num, value):
        self.ne_num = ne_num
        self.subelement_num = subelement_num
        self.value = value
        
        self.set_situation_code()
        self.set_ledger_account()
        self.set_benefits_account()
    
    def set_situation_code(self):
        self.situation_code = 'DFL038'
    
    def set_ledger_account(self):
        self.ledger_account = '3.2.9.1.1.01.00'
    
    def set_benefits_account(self):
        self.benefits_account = '2.1.1.2.1.01.00'
    
    def to_dict(self):
        output_dict = dict(situation_code = self.situation_code,
                           ne_num = self.ne_num,
                           subelement_num = self.subelement_num,
                           ledger_account = self.ledger_account,
                           benefits_account = self.benefits_account,
                           value = self.value)
        
        return output_dict
    
class AuxFunPaymentData():
    def __init__(self, cpf, value):
        self.cpf = cpf
        self.set_cpf_just_numbers()
        self.value = value
        
    def set_cpf_just_numbers(self):
        no_dots = self.cpf.replace('.', '')
        no_dashes = no_dots.replace('-', '')
        self.cpf_just_numbers = no_dashes
    
    def to_dict(self):
        output_dict = dict(cpf = self.cpf_just_numbers,
                           value = self.value)
        
        return output_dict
    
class AuxFunPreDoc():
    def __init__(self, branch_num, account_num, bank_name, deceased_person_name, date_of_death, ap_num, process_num):
        self.branch_num = branch_num
        self.account_num = account_num
        self.bank_name = bank_name.lower()
        self.deceased_person_name = deceased_person_name
        self.date_of_death = date_of_death
        self.ap_num = ap_num
        self.process_num = process_num
        
        self.set_bank_code()
        self.set_gov_bank_code()
        self.set_gov_branch_num()
        self.set_observation()
        
    def set_bank_code(self):
        table = {'itaú': '341',
                 'banco do brasil': '001',
                 'caixa econômica federal': '104'}
        
        self.bank_code = table.get(self.bank_name)
        
        if self.bank_code is None:
            raise Exception(f'Invalid bank name. Got: {self.bank_name}')
        else:
            return
    
    def set_gov_bank_code(self):
        self.gov_bank_code = '001'
    
    def set_gov_branch_num(self):
        self.gov_branch_num = '2234'
    
    def set_observation(self):
        # repetitive. create a class for observation
        self.observation = create_observation(self.deceased_person_name, 
                                              self.date_of_death, self.ap_num, 
                                              self.process_num)
    
    def to_dict(self):
        output_dict = dict(bank_code = self.bank_code, 
                           branch_num = self.branch_num,
                           account_num = self.account_num,
                           gov_bank_code = self.gov_bank_code,
                           gov_branch_num = self.gov_branch_num,
                           observation = self.observation)
        
        return output_dict
    
class AuxFunCostCenter():
    def __init__(self, value):
        self.value = value
        
        self.set_month()
        self.set_year()
        
    def set_month(self):
        formatted_today = today()
        month = formatted_today[3:5]
        self.month = month
    
    def set_year(self):
        formatted_today = today()
        year = formatted_today[6:]
        self.year = year
    
    def to_dict(self):
        output_dict = dict(month = self.month,
                           year = self.year,
                           value = self.value)
        
        return output_dict

def from_string_to_bd_dict(string):
    process_num = pipeline.ProcessNumPipeline().pipeline(string)
    value = pipeline.ValuePipeline().pipeline(string)
    cpf = pipeline.CpfPipeline().pipeline(string)
    ap_date = pipeline.ApDatePipeline().pipeline(string)
    ap_num = pipeline.ApPipeline().pipeline(string)
    date_of_death = pipeline.DateOfDeathPipeline().pipeline(string)
    deceased_person_name = pipeline.DeceasedPersonNamePipeline().pipeline(string)
    
    aux_fun_basic_data = AuxFunBasicData(process_num = process_num, 
                                         value = value, 
                                         cpf = cpf, 
                                         ap_date = ap_date, 
                                         ap_num = ap_num, 
                                         date_of_death = date_of_death, 
                                         deceased_person_name = deceased_person_name)
    bd_dict = aux_fun_basic_data.to_dict()
    return bd_dict

def from_string_to_sd_dict(string):
    ap_num = pipeline.ApPipeline().pipeline(string)
    value = pipeline.ValuePipeline().pipeline(string)
    ap_date = pipeline.ApDatePipeline().pipeline(string)
    
    aux_fun_source_doc = AuxFunSourceDoc(ap_num = ap_num, 
                                         value = value,
                                         ap_date = ap_date)
    sd_dict = aux_fun_source_doc.to_dict()
    return sd_dict

def from_string_to_pd_dict(string):
    ne_num = pipeline.NePipeline().pipeline(string)
    subelement_num = pipeline.SubelementNumPipeline().pipeline(string)
    value = pipeline.ValuePipeline().pipeline(string)
    
    aux_fun_pco = AuxFunPco(ne_num = ne_num, 
                            subelement_num = subelement_num,
                            value = value)
    pd_dict = aux_fun_pco.to_dict()
    return pd_dict

def from_string_to_pay_dict(string):
    cpf = pipeline.CpfPipeline().pipeline(string)
    value = pipeline.ValuePipeline().pipeline(string)
    
    aux_fun_payment_data = AuxFunPaymentData(cpf = cpf, 
                                             value = value)
    pay_dict = aux_fun_payment_data.to_dict()
    return pay_dict

def from_string_to_pre_doc_dict(string):
    branch_num = pipeline.BranchNumPipeline().pipeline(string)
    account_num = pipeline.AccountNumPipeline().pipeline(string)
    bank_name = pipeline.BankNamePipeline().pipeline(string)
    deceased_person_name = pipeline.DeceasedPersonNamePipeline().pipeline(string)
    date_of_death = pipeline.DateOfDeathPipeline().pipeline(string)
    ap_num = pipeline.ApPipeline().pipeline(string)
    process_num = pipeline.ProcessNumPipeline().pipeline(string)
    
    aux_fun_pre_doc = AuxFunPreDoc(branch_num = branch_num, 
                                   account_num = account_num, 
                                   bank_name = bank_name, 
                                   deceased_person_name = deceased_person_name, 
                                   date_of_death = date_of_death, 
                                   ap_num = ap_num, 
                                   process_num = process_num)
    pre_doc_dict = aux_fun_pre_doc.to_dict()
    return pre_doc_dict

def from_string_to_cc_dict(string):
    value = pipeline.ValuePipeline().pipeline(string)
    
    aux_fun_cost_center = AuxFunCostCenter(value = value)
    cc_dict = aux_fun_cost_center.to_dict()
    return cc_dict
