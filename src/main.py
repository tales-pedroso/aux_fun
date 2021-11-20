# -*- coding: utf-8 -*-

from os import path, sep
from glob import glob
import from_pdf_to_string
import ap_builder
import dh_creation

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

CPF = ''       # set your credentials
PASSWORD = ''  # set your credentials

SRC_FOLDER = path.dirname(__file__)
ROOT_FOLDER = path.dirname(SRC_FOLDER)
APS_FOLDER = ROOT_FOLDER + sep + 'aps'
PDF_FILES = glob(APS_FOLDER + sep + '*.pdf')
GECKODRIVER_PATH = ROOT_FOLDER + sep + 'depend' + sep + 'geckodriver.exe'

def get_dicts_from_pdf(pdf):
    string = from_pdf_to_string.get_processed_string_from_pdf(pdf)
    bd_dict = ap_builder.from_string_to_bd_dict(string)
    sd_dict = ap_builder.from_string_to_sd_dict(string)
    pd_dict = ap_builder.from_string_to_pd_dict(string)
    pay_dict = ap_builder.from_string_to_pay_dict(string)
    pre_doc_dict = ap_builder.from_string_to_pre_doc_dict(string)
    cc_dict = ap_builder.from_string_to_cc_dict(string)
    
    dicts = dict(bd_dict = bd_dict,
                 sd_dict = sd_dict,
                 pd_dict = pd_dict,
                 pay_dict = pay_dict,
                 pre_doc_dict = pre_doc_dict,
                 cc_dict = cc_dict)
    return dicts

if __name__ == '__main__':
    # init driver
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service = service)
    driver.maximize_window()
    
    dh_creation.log_in_to_siafi(driver, CPF, PASSWORD)
    
    for pdf in PDF_FILES:
        dicts = get_dicts_from_pdf(pdf)
    
        dh_creation.go_to_incdh(driver)
        dh_creation.include_fl(driver)
    
        dh_creation.create_basic_data(driver, dicts['bd_dict'])
        dh_creation.check_basic_data(driver, dicts['bd_dict'])
    
        dh_creation.create_source_doc(driver, dicts['sd_dict'])
        dh_creation.check_source_doc(driver, dicts['sd_dict'])
        dh_creation.confirm_source_doc(driver)
    
        dh_creation.confirm_basic_data_tab(driver)
    
        dh_creation.create_pco(driver, dicts['pd_dict'])
        dh_creation.check_pco(driver, dicts['pd_dict'])
        dh_creation.confirm_pco(driver)
        dh_creation.from_pco_to_payment_data(driver)
    
        dh_creation.create_payment_data_tab(driver)
        dh_creation.set_payment_data_tab(driver, dicts['pay_dict'])
        dh_creation.check_payment_data_tab(driver, dicts['pay_dict'])
        dh_creation.confirm_payment_data_row(driver)
        dh_creation.from_payment_data_to_pre_doc(driver)
    
        dh_creation.set_pre_doc(driver, dicts['pre_doc_dict'])
        dh_creation.check_pre_doc(driver, dicts['pre_doc_dict'])
        dh_creation.confirm_pre_doc(driver)
        dh_creation.from_pre_doc_to_cost_center(driver)
    
        dh_creation.set_cost_center(driver, dicts['cc_dict'])
        dh_creation.check_cost_center(driver, dicts['cc_dict'])
        dh_creation.confirm_cost_center(driver, dicts['cc_dict'])
    
        dh_creation.register_dh(driver)
        dh = dh_creation.get_dh(driver)
        dh_creation.return_from_dh_panel(driver)
        
        print(dh)
        
        
        
        
        
    
    

