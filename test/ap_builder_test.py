# -*- coding: utf-8 -*-

import unittest
from os import chdir, path, sep

test_folder = path.dirname(__file__)
root_folder = path.dirname(test_folder)
chdir(root_folder + sep + 'src')

from ap_builder import (today, AuxFunBasicData, AuxFunSourceDoc, AuxFunPco, AuxFunPaymentData,
                        AuxFunPreDoc, AuxFunCostCenter)

class AuxFunBasicDataTest(unittest.TestCase):
    def test_returns_dict_with_expected_values(self):
        expected_dict = dict(due_date = today(), 
                             process_num = '0045142.00001057/2021-07',
                             truncated_process_num = '45142.001057/2021-07',
                             validation_date = '15/02/2021',
                             value = '15.689,37',
                             recipient = '11111111111',
                             observation = 'Pagamento do auxílio-funeral de João Silveira Costa e Filho, falecido/a em 01/01/2021. AP 35/2021. Processo: 0045142.00001057/2021-07.')
        
        aux_fun_basic_data = AuxFunBasicData(process_num = '0045142.00001057/2021-07',
                                             value = '15.689,37',
                                             cpf = '111.111.111-11',
                                             ap_date = '15/02/2021',
                                             ap_num = '35/2021',
                                             date_of_death = '01/01/2021',
                                             deceased_person_name = 'João Silveira Costa e Filho')
        
        output_dict = aux_fun_basic_data.to_dict()
        self.assertEqual(output_dict, expected_dict)

class AuxFunSourceDocTest(unittest.TestCase):
    def test_returns_dict_with_expected_values(self):
        expected_dict = dict(doc_emitter = '114601',
                             ap_num = 'AP 304/2021',
                             ap_date = '01/01/2021',
                             value = '1.024,47')
        
        aux_fun_source_doc = AuxFunSourceDoc(ap_num = '304/2021',
                                             ap_date = '01/01/2021',
                                             value = '1.024,47')
        
        output_dict = aux_fun_source_doc.to_dict()
        self.assertEqual(output_dict, expected_dict)

class AuxFunPcoTest(unittest.TestCase):
    def test_returns_dict_with_expected_values(self):
        expected_dict = dict(situation_code = 'DFL038',
                             ne_num = '2021NE000028',
                             subelement_num = '01',
                             ledger_account = '3.2.9.1.1.01.00',
                             benefits_account = '2.1.1.2.1.01.00',
                             value = '99,75')
        
        aux_fun_pco = AuxFunPco(ne_num = '2021NE000028',
                                subelement_num = '01',
                                value = '99,75')
        
        output_dict = aux_fun_pco.to_dict()
        self.assertEqual(output_dict, expected_dict)
        
class AuxFunPaymentDataTest(unittest.TestCase):
    def test_returns_dict_with_expected_values(self):
        expected_dict = dict(cpf = '36912843883',
                             value = '693.261.000,52')
        aux_fun_payment_data = AuxFunPaymentData(cpf = '369.128.438-83', 
                                                 value = '693.261.000,52')
        
        output_dict = aux_fun_payment_data.to_dict()
        self.assertEqual(output_dict, expected_dict)

class AuxFunPreDocTest(unittest.TestCase):
    def test_returns_dict_with_expected_values_when_bank_is_itau(self):
        expected_dict = dict(bank_code = '341', 
                             branch_num = '6317',
                             account_num = '54838',
                             gov_bank_code = '001',
                             gov_branch_num = '2234',
                             observation = 'Pagamento do auxílio-funeral de JOÃO MARINHO, falecido/a em 06/08/2021. AP 225/2021. Processo: 45142.001179/2021-26.')
        
        aux_fun_pre_doc = AuxFunPreDoc(branch_num = '6317', 
                                       account_num = '54838', 
                                       bank_name = 'ITAÚ', 
                                       deceased_person_name = 'JOÃO MARINHO', 
                                       date_of_death = '06/08/2021', 
                                       ap_num = '225/2021', 
                                       process_num = '45142.001179/2021-26')
        
        output_dict = aux_fun_pre_doc.to_dict()
        self.assertEqual(output_dict, expected_dict)
        
    def test_returns_dict_with_expected_values_when_bank_is_bb(self):
        expected_dict = dict(bank_code = '001', 
                             branch_num = '6317',
                             account_num = '54838',
                             gov_bank_code = '001',
                             gov_branch_num = '2234',
                             observation = 'Pagamento do auxílio-funeral de JOÃO MARINHO, falecido/a em 06/08/2021. AP 225/2021. Processo: 45142.001179/2021-26.')
        
        aux_fun_pre_doc = AuxFunPreDoc(branch_num = '6317', 
                                       account_num = '54838', 
                                       bank_name = 'BANCO DO BRASIL', 
                                       deceased_person_name = 'JOÃO MARINHO', 
                                       date_of_death = '06/08/2021', 
                                       ap_num = '225/2021', 
                                       process_num = '45142.001179/2021-26')
        
        output_dict = aux_fun_pre_doc.to_dict()
        self.assertEqual(output_dict, expected_dict)
        
    def test_returns_dict_with_expected_values_when_bank_is_cef(self):
        expected_dict = dict(bank_code = '104', 
                             branch_num = '6317',
                             account_num = '54838',
                             gov_bank_code = '001',
                             gov_branch_num = '2234',
                             observation = 'Pagamento do auxílio-funeral de JOÃO MARINHO, falecido/a em 06/08/2021. AP 225/2021. Processo: 45142.001179/2021-26.')
        
        aux_fun_pre_doc = AuxFunPreDoc(branch_num = '6317', 
                                       account_num = '54838', 
                                       bank_name = 'CAIXA ECONÔMICA FEDERAL', 
                                       deceased_person_name = 'JOÃO MARINHO', 
                                       date_of_death = '06/08/2021', 
                                       ap_num = '225/2021', 
                                       process_num = '45142.001179/2021-26')
        
        output_dict = aux_fun_pre_doc.to_dict()
        self.assertEqual(output_dict, expected_dict)
        
class AuxFunCostCenterTest(unittest.TestCase):
    def test_returns_dict_with_expected_values(self):
        expected_dict = dict(month = today()[3:5], 
                             year = today()[6:],
                             value = '0,01')
        
        aux_fun_cost_center = AuxFunCostCenter(value = '0,01')
        output_dict = aux_fun_cost_center.to_dict()
        self.assertEqual(output_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()
