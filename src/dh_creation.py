# -*- coding: utf-8 -*-

# create a function from_table_to_page_object to generate code for page objects
# name (str), id (str), set (bool), get(bool), click(bool), advance(bool), check(bool)
# from this table, generate code in .py file
# separate page objects from higher level functions
# define a decorator to try again if it hits StaleElement. usable in click(), set_() and check()

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, any_of                                                           
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from re import search, VERBOSE

#==================================================================================================================
class PageObject():
    '''
    base class with the most used functions by the other page objects
    '''
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        
    def get(self, id_):
        return self.wait.until(element_to_be_clickable((By.ID, id_)))

    def set_(self, id_, value):
        try:
            elem = self.get(id_)
            elem.clear()
            elem.send_keys(value)
        except StaleElementReferenceException:
            print('hit stale element')
            self.set_(id_, value)
    
    def set_date(self, id_, date):
        # fix the name. other inputs other than date also require this method
        elem = self.get(id_)
        elem.clear()
        self.driver.execute_script("arguments[0].value = arguments[1]", 
                                   elem, date)
        
    def check(self, id_, expected_value):
        try:
            elem = self.get(id_)
            return elem.get_attribute('value') == expected_value
        except StaleElementReferenceException:
            print('hit stale element')
            self.check_(id_, expected_value)

    def advanced(self, id_):
        self.get(id_)
        return True
    
    def click(self, id_):
        elem = self.get(id_)
        elem.click()

#==================================================================================================================
class SiafiAuth(PageObject):
    authentication_url = 'https://siafi.tesouro.gov.br'
    cpf_input_id = 'j_username'
    password_input_id = 'j_password'
    captcha_input_id = 'j_captcha'
    already_open_session_btn_id = 'formRemoverContexto:botaoConfirmar'
    accept_terms_btn_id = 'frmTemplateAcesso:btnConcordar'
    search_input_btn_id = 'frmMenu:acessoRapido'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def go_to_authentication_page(self):
        self.driver.get(self.authentication_url)
        
    def set_cpf(self, cpf):
        self.set_(self.cpf_input_id, cpf)
        
    def set_password(self, password):
        self.set_(self.password_input_id, password)
        
    def put_focus_on_captcha_input(self):
        self.click(self.captcha_input_id)
        
    def detect_captcha_resolution(self):
        condition1 = element_to_be_clickable((By.ID, self.already_open_session_btn_id))
        condition2 = element_to_be_clickable((By.ID, self.accept_terms_btn_id))
        conditions = (condition1, condition2)
        
        # waits until one of the 2 buttons shows up for 100 seconds
        self.wait = WebDriverWait(self.driver, timeout = 100)
        
        # get the first button that appears
        elem = self.wait.until(any_of(*conditions))
        
        # restore initial timeout conditions
        self.wait = WebDriverWait(self.driver, 15)
        
        # figure out which button is it
        matched_btn = elem.get_attribute('id')
        
        # if it is "accept terms", simply click it and move on
        if matched_btn == self.accept_terms_btn_id:
            elem.click()
            return
        
        # if it is "already open session", click it
        elif matched_btn == self.already_open_session_btn_id:
            elem.click()
            
            # then wait for "accept terms" and click it too
            elem = self.wait.until(condition2)
            elem.click()
            return
        
    def advanced_to_initial_page(self):
        return self.advanced(self.search_input_btn_id)

#==================================================================================================================
class SiafiInitialPage(PageObject):
    search_input_id = 'frmMenu:acessoRapido'
    submit_btn_id = 'frmMenu:botaoAcessoRapidoVerificaTipoTransacao'
    dh_input_id = 'form_manterDocumentoHabil:codigoTipoDocHabil_input'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def set_search_text(self, search_text):
        self.set_(self.search_input_id, search_text)
        
    def check_search_text(self, expected_text):
        return self.check(self.search_input_id, expected_text)
        
    def submit_search(self):
        # standardize this. call it click
        self.click(self.submit_btn_id)
        
    def advanced_to_incdh(self):
        return self.advanced(self.dh_input_id)

#==================================================================================================================
class IncdhInitialPage(SiafiInitialPage):
    confirm_btn_id = 'form_manterDocumentoHabil:btnConfirmarTipoDoc'
    dh_title_id = 'form_manterDocumentoHabil:tituloTipoDocHabil'
    ug_input_id = 'form_manterDocumentoHabil:pagadoraRecebedora'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def set_dh(self, dh):
        self.set_(self.dh_input_id, dh) # inherited from SiafiInitialPage
        
    def check_dh_title(self, expected_text):
        condition = lambda d: d.find_element(By.ID, self.dh_title_id).get_attribute('innerHTML') == expected_text
        self.wait.until(condition)
        
        return True
        
    def submit(self):
        # standardize this. call it click
        self.click(self.confirm_btn_id)
        
    def advanced_to_dh_basic_data(self):
        return self.advanced(self.ug_input_id)
    
#==================================================================================================================
class BasicData(PageObject):
    due_date_input_id = 'form_manterDocumentoHabil:dataVencimento_calendarInputDate'
    process_num_input_id = 'form_manterDocumentoHabil:processo_input'
    validation_date_input_id = 'form_manterDocumentoHabil:dataAteste_calendarInputDate'
    value_input_id = 'form_manterDocumentoHabil:valorPrincipalDocumento_input'
    recipient_input_id = 'form_manterDocumentoHabil:credorDevedor_input' # may throw StaleElement when checking
    observation_textarea_id = 'form_manterDocumentoHabil:observacao'
    doc_emitter_input_id = 'form_manterDocumentoHabil:tableDocsOrigem:0:emitenteDocOrigem_input'
    recipient_name_id = 'form_manterDocumentoHabil:nomeCredorDevedor'
    confirm_basic_data_btn_id = 'form_manterDocumentoHabil:btnConfirmarDadosBasicos'
    pco_tab_id = 'form_manterDocumentoHabil:abaPrincipalComOrcamentoId'
    pco_situation_input_id = 'form_manterDocumentoHabil:campo_situacao_input'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def set_due_date(self, due_date):
        self.set_date(self.due_date_input_id, due_date)
        
    def set_process_num(self, process_num):
        self.set_(self.process_num_input_id, process_num)
        
    def set_validation_date(self, validation_date):
        self.set_date(self.validation_date_input_id, validation_date)
        
    def set_value(self, value):
        self.set_(self.value_input_id, value)
        
    def set_recipient(self, recipient):
        self.set_(self.recipient_input_id, recipient)
        
    def set_observation(self, observation):
        self.set_(self.observation_textarea_id, observation)
    
    def is_recipient_name_loaded(self):
        # standardize this. call it check
        condition = lambda d: d.find_element(By.ID, self.recipient_name_id).get_attribute('innerHTML') != ''
        
        try:
            self.wait.until(condition)
            return True
        except TimeoutException:
            print("Recipient is not registered yet")
            return False
        
    def check_due_date(self, expected_due_date):
        return self.check(self.due_date_input_id, expected_due_date)
        
    def check_process_num(self, expected_process_num):
        return self.check(self.process_num_input_id, expected_process_num)
    
    def check_validation_date(self, expected_validation_date):
        return self.check(self.validation_date_input_id, expected_validation_date)
    
    def check_value(self, expected_value):
        return self.check(self.value_input_id, expected_value)
    
    def check_recipient(self, expected_recipient):
        return self.check(self.recipient_input_id, expected_recipient)
    
    def check_observation(self, expected_observation):
        return self.check(self.observation_textarea_id, expected_observation)
        
    def click_confirm_basic_data_btn(self):
        self.click(self.confirm_basic_data_btn_id)
        
    def is_pco_clickable(self):
        return self.advanced(self.pco_tab_id)
    
    def click_pco_tab(self):
        # may throw StaleElementReferenceException, which is not treated so far
        self.click(self.pco_tab_id)
    
    def advanced_to_pco(self):
        return self.advanced(self.pco_situation_input_id)
    
    # it does not have a method to evaluate errors in Siafi's validation
    # errors are class="error"
    # also, it throws TimeoutException without saying anything. encapsulate that to return a meaningful message
    
#==================================================================================================================    
class SourceDoc(PageObject):
    include_source_doc_btn_id = 'form_manterDocumentoHabil:tableDocsOrigem_painel_incluir'
    doc_emitter_input_id = 'form_manterDocumentoHabil:tableDocsOrigem:0:emitenteDocOrigem_input'
    doc_date_input_id = 'form_manterDocumentoHabil:tableDocsOrigem:0:dataEmissaoDocOrigem_calendarInputDate'
    doc_num_input_id = 'form_manterDocumentoHabil:tableDocsOrigem:0:numeroDocOrigem_input'
    doc_value_input_id = 'form_manterDocumentoHabil:tableDocsOrigem:0:valorDocOrigem_input'
    doc_confirm_btn_id = 'form_manterDocumentoHabil:tableDocsOrigem_painel_confirmar'
    first_doc_checkbtn_id = 'form_manterDocumentoHabil:tableDocsOrigem:0:tableDocsOrigem_check_selecao'
        
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_include_source_doc(self):
        self.click(self.include_source_doc_btn_id)
        
    def did_it_include_source_doc(self):
        # standardize this. there is checking an input and there is checking if it advanced
        # assumes there is only one source doc
        return self.advanced(self.doc_emitter_input_id)
    
    def set_doc_emitter(self, doc_emitter):
        self.set_(self.doc_emitter_input_id, doc_emitter)
        
    def set_doc_date(self, doc_date):
        self.set_date(self.doc_date_input_id, doc_date)
        
    def set_doc_num(self, doc_num):
        self.set_(self.doc_num_input_id, doc_num)
        
    def set_doc_value(self, doc_value):
        self.set_(self.doc_value_input_id, doc_value)
        
    def check_doc_emitter(self, expected_doc_emitter):
        return self.check(self.doc_emitter_input_id, expected_doc_emitter)
    
    def check_doc_date(self, expected_doc_date):
        return self.check(self.doc_date_input_id, expected_doc_date)
    
    def check_doc_num(self, expected_doc_num):
        return self.check(self.doc_num_input_id, expected_doc_num)
    
    def check_doc_value(self, expected_doc_value):
        return self.check(self.doc_value_input_id, expected_doc_value)
    
    def click_confirm_btn(self):
        self.click(self.doc_confirm_btn_id)
        
    def did_it_confirm_source_doc(self):
        return self.advanced(self.first_doc_checkbtn_id)
        
#==================================================================================================================
class Pco(PageObject):
    situation_input_id = 'form_manterDocumentoHabil:campo_situacao_input'
    confirm_situation_btn_id = 'form_manterDocumentoHabil:botao_ConfirmarSituacao'
    ne_input_id = 'form_manterDocumentoHabil:lista_PCO:0:PCO_item_num_empenho_input'
    subelement_input_id = 'form_manterDocumentoHabil:lista_PCO:0:PCO_item_num_subitem_input'
    ledger_account_input_id = 'form_manterDocumentoHabil:lista_PCO:0:PCO_item_campoClassificacaoA_input_classificacao_contabil'
    benefits_account_input_id = 'form_manterDocumentoHabil:lista_PCO:0:PCO_item_campoClassificacaoB_input_classificacao_contabil'
    value_input_id = 'form_manterDocumentoHabil:lista_PCO:0:PCO_item_valor_item_input'
    confirm_btn_id = 'form_manterDocumentoHabil:lista_PCO_painel_confirmar'
    pco_created_checkbox_id = 'form_manterDocumentoHabil:lista_PCO:0:painel_collapse_PCO_selecao'
    payment_data_tab_id = 'form_manterDocumentoHabil:abaDadosPagRecId'
    payment_data_table_checkbox_id = 'form_manterDocumentoHabil:lista_DPgtoOB:siafiTableCheck_DP_OB_cabecalho'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def set_situation_code(self, situation_code):
        self.set_(self.situation_input_id, situation_code)
        
    def check_situation_code(self, expected_situation_code):
        return self.check(self.situation_input_id, expected_situation_code)
        
    def click_confirm_situation_btn(self):
        self.click(self.confirm_situation_btn_id)
        
    def set_ne(self, ne):
        self.set_(self.ne_input_id, ne)
    
    def set_subelement(self, subelement):
        self.set_date(self.subelement_input_id, subelement)
    
    def set_ledger_account(self, ledger_account):
        self.set_date(self.ledger_account_input_id, ledger_account)
        
    def set_benefits_account(self, benefits_account):
        self.set_date(self.benefits_account_input_id, benefits_account)
        
    def set_value(self, value):
        self.set_(self.value_input_id, value)
    
    def check_ne(self, expected_ne):
        return self.check(self.ne_input_id, expected_ne)
    
    def check_subelement(self, expected_subelement):
        return self.check(self.subelement_input_id, expected_subelement)
    
    def check_ledger_account(self, expected_ledger_account):
        return self.check(self.ledger_account_input_id, expected_ledger_account)
    
    def check_benefits_account(self, expected_benefits_account):
        return self.check(self.benefits_account_input_id, expected_benefits_account)
    
    def check_value(self, expected_value):
        return self.check(self.value_input_id, expected_value)
    
    def click_confirm_btn(self):
        self.click(self.confirm_btn_id)
        
    def is_pco_created(self):
        return self.advanced(self.pco_created_checkbox_id)
    
    def click_payment_data_tab(self):
        self.click(self.payment_data_tab_id)
        
    def advanced_to_payment_data(self):
        return self.advanced(self.payment_data_table_checkbox_id)
    
class PaymentData(PageObject):
    include_row_btn_id = 'form_manterDocumentoHabil:lista_DPgtoOB_painel_incluir'
    recipient_input_id = 'form_manterDocumentoHabil:lista_DPgtoOB:0:codigoFavorecido_input'
    value_input_id = 'form_manterDocumentoHabil:lista_DPgtoOB:0:valorPredoc_input'
    confirm_row_btn_id = 'form_manterDocumentoHabil:lista_DPgtoOB_painel_confirmar'
    first_row_checkbox_id = 'form_manterDocumentoHabil:lista_DPgtoOB:0:siafiTableCheck_DP_OB_selecao'
    predoc_btn_id = 'form_manterDocumentoHabil:lista_DPgtoOB:0:btnPredoc'
    bank_code_input_id = 'form_manterDocumentoHabil:favorecido_banco_input'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def click_include_row_btn(self):
        self.click(self.include_row_btn_id)

    def did_it_include_row(self): # buggy
        return self.advanced(self.recipient_input_id)
        
    def set_recipient(self, recipient):
        self.set_(self.recipient_input_id, recipient)
    
    def set_value(self, value):
        self.set_(self.value_input_id, value)
    
    def check_recipient(self, expected_recipient):
        return self.check(self.recipient_input_id, expected_recipient)
    
    def check_value(self, expected_value):
        return self.check(self.value_input_id, expected_value)

    def click_confirm_row(self):
        self.click(self.confirm_row_btn_id)
    
    def is_first_row_created(self):
        return self.advanced(self.first_row_checkbox_id)
    
    def click_pre_doc(self):
        self.click(self.predoc_btn_id)
    
    def advanced_to_pre_doc(self):
        return self.advanced(self.bank_code_input_id)
    
class PreDoc(PageObject):
    bank_code_input_id = 'form_manterDocumentoHabil:favorecido_banco_input'
    branch_num_input_id = 'form_manterDocumentoHabil:favorecido_agencia_input'
    account_num_input_id = 'form_manterDocumentoHabil:favorecido_conta_input'
    gov_bank_code_input_id = 'form_manterDocumentoHabil:pagador_banco_input'
    gov_branch_num_input_id = 'form_manterDocumentoHabil:pagador_agencia_input'
    observation_textarea_id = 'form_manterDocumentoHabil:observacaoPredoc'
    confirm_btn_id = 'form_manterDocumentoHabil:btnConfirmarPredoc'
    cost_center_btn_id = 'form_manterDocumentoHabil:abaCentroCustoId' # gets intercepted
    cost_center_month_input_id = 'form_manterDocumentoHabil:cvMesReferenciaCentroCusto_input'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def set_bank_code(self, bank_code):
        self.set_(self.bank_code_input_id, bank_code)
        
    def set_branch_num(self, branch_num):
        self.set_(self.branch_num_input_id, branch_num)
    
    def set_account_num(self, account_num):
        self.set_(self.account_num_input_id, account_num)
        
    def set_gov_bank_code(self, gov_bank_code):
        self.set_(self.gov_bank_code_input_id, gov_bank_code)
        
    def set_gov_branch_num(self, gov_branch_num):
        self.set_(self.gov_branch_num_input_id, gov_branch_num)
        
    def set_observation(self, observation):
        self.set_(self.observation_textarea_id, observation)
        
    def check_bank_code(self, expected_bank_code):
        return self.check(self.bank_code_input_id, expected_bank_code)
    
    def check_branch_num(self, expected_branch_num):
        return self.check(self.branch_num_input_id, expected_branch_num)
    
    def check_account_num(self, expected_account_num):
        return self.check(self.account_num_input_id, expected_account_num)
    
    def check_gov_bank_code(self, expected_gov_bank_code):
        return self.check(self.gov_bank_code_input_id, expected_gov_bank_code)
    
    def check_gov_branch_num(self, expected_gov_branch_num):
        return self.check(self.gov_branch_num_input_id, expected_gov_branch_num)
    
    def check_observation(self, expected_observation):
        return self.check(self.observation_textarea_id, expected_observation)
    
    def click_confirm_btn(self):
        self.click(self.confirm_btn_id)
        
    def is_predoc_confirmed(self):
        return self.advanced(self.cost_center_btn_id)
    
    def click_cost_center(self):
        # remove infinite loop and set a fixed number of times to try it
        while True:
            try:
                self.click(self.cost_center_btn_id)
                break
            except ElementClickInterceptedException:
                print('click intercepted')
                time.sleep(0.1)

    def advanced_to_cost_center(self):
        return self.advanced(self.cost_center_month_input_id)

class CostCenter(PageObject):
    first_row_checkbox_id = 'form_manterDocumentoHabil:consolidado_dataTable:0:consolidado_subTable:0:consolidado_checkBox__'
    month_input_id = 'form_manterDocumentoHabil:cvMesReferenciaCentroCusto_input'
    year_input_id = 'form_manterDocumentoHabil:cvAnoReferenciaCentroCusto_input'
    include_btn_id = 'form_manterDocumentoHabil:btnIncluirNovoVinculoCentroCusto'
    total_cost_text_id = 'form_manterDocumentoHabil:centroCusto_informado_toogle_panel_valor_total'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def click_first_row_checkbox(self):
        self.click(self.first_row_checkbox_id)
        
    def set_month(self, month):
        self.set_(self.month_input_id, month)
        
    def set_year(self, year):
        self.set_(self.year_input_id, year)
        
    def check_month(self, expected_month):
        return self.check(self.month_input_id, expected_month)
        
    def check_year(self, expected_year):
        return self.check(self.year_input_id, expected_year)
        
    def click_confirm(self):
        self.click(self.include_btn_id)
        
    def check_total_cost(self, expected_value):
        condition = lambda d: d.find_element(By.ID, self.total_cost_text_id).get_attribute('innerHTML') == expected_value
        self.wait.until(condition)
        
        return True

class Register(PageObject):
    register_dh_btn_id = 'form_manterDocumentoHabil:btnRegistrar'
    notification_text_id = 'form_manterDocumentoHabil:tableNsGeradas:0:outOrigem'
    return_btn_id = 'form_manterDocumentoHabil:btnRetornarResultadoRegistrar'
    dh_num_text_id = 'form_manterDocumentoHabil:numeroDocumentoHabil_outputText'
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def click_register_dh(self):
        self.click(self.register_dh_btn_id)
        
    def advanced_to_registered_panel(self):
        return self.advanced(self.notification_text_id)
    
    def extract_string_in_class_legend(self): # delegate to some string processing class
        elem = self.wait.until(element_to_be_clickable((By.CLASS_NAME, 'legend')))
        string = elem.text
        
        return string
    
    def check_string_in_class_legend(self, string): # delegate to some string processing class
        right = string.startswith('Número do Documento Hábil Registrado: ')
        
        pattern = '(\d{4}FL\d{6})$'
        match = search(pattern, string, VERBOSE)
        
        if (match is None) or (not right):
            raise Exception('Failed to extract DH number')
        else:
            dh = match.groups()[0]
            return dh
            
    def click_return_btn(self):
        self.click(self.return_btn_id)
    
    def returned_to_incdh(self):
        return self.advanced(self.dh_num_text_id)


#==================================================================================================================
#==================================================================================================================
# HIGH-LEVEL FUNCTIONS

# they always get a page object, call methods and pass values
# can I make them into classes? with zip(method_list, args_list)
# they are just a bunch of setters, a bunch of checkers, a page object, and a few transitions (advanced)
# after Exception, it cannot execute go_to_incdh() then include_fl()
# it stops there
# sometimes the website throws 500 error code when filling source_doc data
# high-level functions may be Setter, Checker, Transition (from tabs and server responses), 

def log_in_to_siafi(driver, cpf, password):
    # get page object
    siafi_auth = SiafiAuth(driver)
    
    # go to initial page
    siafi_auth.go_to_authentication_page()
    
    # type cpf and password
    siafi_auth.set_cpf(cpf)
    siafi_auth.set_password(password)
    
    # put the focus on captcha resolution so that the user doesn't have to do that
    siafi_auth.put_focus_on_captcha_input()

    # wait until driver advances to next page
    siafi_auth.detect_captcha_resolution()
    
    # if everything went right, return next page object
    if siafi_auth.advanced_to_initial_page():
        print("Advanced to Siafi's initial page")
        return 
    else:
        raise Exception("Failed to advance to Siafi's initial page")

def go_to_incdh(driver):
    # get page object
    siafi_initial_page = SiafiInitialPage(driver)
    
    # put 'incdh' on search bar
    siafi_initial_page.set_search_text('incdh')
    
    # make sure the text is 'incdh' before submitting
    if siafi_initial_page.check_search_text('incdh'):
        siafi_initial_page.submit_search()
    else:
        raise Exception("Failed to type incdh on Siafi's search bar")
        
    if siafi_initial_page.advanced_to_incdh():
        print("Advanced to INCDH section")
        return
    else:
        raise Exception("Failed to advance to INCDH")

def include_fl(driver):
    # get page object
    incdh_initial_page = IncdhInitialPage(driver)
    
    # set dh as FL
    incdh_initial_page.set_dh('FL')
    
    # async JavaScript call inserts title after we input a valid DH type. check if it is right
    if incdh_initial_page.check_dh_title('FOLHA DE PAGAMENTO'):
        
        # hit the confirm button
        incdh_initial_page.submit()
        
        # check if it advanced
        if incdh_initial_page.advanced_to_dh_basic_data():
            print('Advanced to FL creation')
            return
    else:
        raise Exception('Failed to create a FL in INCDH initial page')
        
def create_basic_data(driver, basic_data_dict): 
    # get page object
    basic_data = BasicData(driver)
    
    # set values into input/textarea
    basic_data.set_due_date(basic_data_dict['due_date'])
    basic_data.set_process_num((basic_data_dict['truncated_process_num']))
    basic_data.set_validation_date(basic_data_dict['validation_date'])
    basic_data.set_value(basic_data_dict['value'])
    basic_data.set_recipient(basic_data_dict['recipient'])
    basic_data.set_observation(basic_data_dict['observation'])
    
    print('Filled Basic Data Tab')
    
def check_basic_data(driver, basic_data_dict):
    # get page object
    basic_data = BasicData(driver)
    
    # confirm input values
    right = True
    
    right = right and basic_data.check_due_date(basic_data_dict['due_date'])
    right = right and basic_data.check_process_num(basic_data_dict['truncated_process_num'])
    right = right and basic_data.check_validation_date(basic_data_dict['validation_date'])
    right = right and basic_data.check_value(basic_data_dict['value'])
    right = right and basic_data.check_recipient(basic_data_dict['recipient'])
    right = right and basic_data.check_observation(basic_data_dict['observation'])
    right = right and basic_data.is_recipient_name_loaded()
    
    if right:
        print('Basic Data tab values match their expected values')
        return
    else:
        raise Exception('Basic Data tab values do not match their expected value')
    
def create_source_doc(driver, source_doc_dict):
    # get page object
    source_doc = SourceDoc(driver)
    
    # hit button to include source document
    source_doc.click_include_source_doc()
    
    # check if it actually included
    if source_doc.did_it_include_source_doc():
          
        # set values into input
        source_doc.set_doc_emitter(source_doc_dict['doc_emitter'])
        source_doc.set_doc_date(source_doc_dict['ap_date'])
        source_doc.set_doc_num(source_doc_dict['ap_num'])
        source_doc.set_doc_value(source_doc_dict['value'])
        
        print('Filled Source Document')
        
    else:
        raise Exception('Failed to include a source document inside Basic Data tab')
    
def check_source_doc(driver, source_doc_dict):
    # get page object
    source_doc = SourceDoc(driver)
    
    # confirm input values
    right = True
    
    right = right and source_doc.check_doc_emitter(source_doc_dict['doc_emitter'])
    right = right and source_doc.check_doc_date(source_doc_dict['ap_date'])
    right = right and source_doc.check_doc_num(source_doc_dict['ap_num'])
    right = right and source_doc.check_doc_value(source_doc_dict['value'])
    
    if right:
        print('Source document values match their expected values')
        return
    else:
        raise Exception('Source document values do not match their expected value')
        
def confirm_source_doc(driver):
    # get page object
    source_doc = SourceDoc(driver)
    
    # hit confirm
    source_doc.click_confirm_btn()
    
    # check it if there a new line in the table of source documents
    if source_doc.did_it_confirm_source_doc():
        print('Confirmed the source document creation')
        return
    
    else:
        raise Exception('Failed to confirm the source doc creation')
        
def confirm_basic_data_tab(driver):
    # it is not separation of concerns here. there should be one func for clicking and another to advance
    basic_data = BasicData(driver)
    
    basic_data.click_confirm_basic_data_btn()
    
    if basic_data.is_pco_clickable():
        basic_data.click_pco_tab()
        
        if basic_data.advanced_to_pco():
            print('Advanced to PCO tab')
        
        return
    else:
        raise Exception('Failed to confirm Basic Data tab and advance to PCO tab')
        
def create_pco(driver, pco_dict):
    pco = Pco(driver)
    
    pco.set_situation_code(pco_dict['situation_code'])
    pco.click_confirm_situation_btn()
    
    pco.set_ne(pco_dict['ne_num'])
    pco.set_subelement(pco_dict['subelement_num'])
    pco.set_ledger_account(pco_dict['ledger_account'])
    pco.set_benefits_account(pco_dict['benefits_account'])
    pco.set_value(pco_dict['value'])
        
def check_pco(driver, pco_dict):
    pco = Pco(driver)
    
    # confirm input values
    right = True
    
    right = right and pco.check_ne(pco_dict['ne_num'])
    right = right and pco.check_subelement(pco_dict['subelement_num'])
    right = right and pco.check_ledger_account(pco_dict['ledger_account'])
    right = right and pco.check_benefits_account(pco_dict['benefits_account'])
    right = right and pco.check_value(pco_dict['value'])
    
    if right:
        print('PCO tab values match their expected values')
        return
    else:
        raise Exception('PCO tab values do not match their expected value')
        
def confirm_pco(driver):
    pco = Pco(driver)
    
    pco.click_confirm_btn()
    
    if pco.is_pco_created():
        print('Created a PCO tab')
        return
    else:
        raise Exception('Failed to create a PCO tab')
        
def from_pco_to_payment_data(driver):
    pco = Pco(driver)
    
    pco.click_payment_data_tab()
    
    if pco.advanced_to_payment_data():
        print('Advanced to Payment Data tab')
        return
    else:
        raise Exception('Failed to advance to Payment Data tab')

def create_payment_data_tab(driver):        
    payment_data = PaymentData(driver)
    
    payment_data.click_include_row_btn()
    if payment_data.did_it_include_row(): # buggy
        print('Included a row in Payment Data tab')
        return
    else:
        raise Exception('Failed to include row in Payment Data tab')
        
def set_payment_data_tab(driver, pay_dict):
    payment_data = PaymentData(driver)
    
    payment_data.set_recipient(pay_dict['cpf'])
    payment_data.set_value(pay_dict['value'])
    
def check_payment_data_tab(driver, pay_dict):
    payment_data = PaymentData(driver)
    
    right = True
    
    right = right and payment_data.check_recipient(pay_dict['cpf'])
    right = right and payment_data.check_value(pay_dict['value'])
    
    if right:
        print('Payment Data tab values match their expected values')
        return 
    else:
        raise Exception('Payment Data tab values do not match their expected value')
    
def confirm_payment_data_row(driver):
    payment_data = PaymentData(driver)
    
    payment_data.click_confirm_row()
    if payment_data.is_first_row_created():
        print('Confirmed a row inclusion in Payment Data tab')
        return
    else:
        raise Exception('Failed to confirm a row inclusion in Payment Data tab')
        
def from_payment_data_to_pre_doc(driver):
    payment_data = PaymentData(driver)
    
    payment_data.click_pre_doc()
    if payment_data.advanced_to_pre_doc():
        print('Advanced to Pre Doc')
        return
    else:
        raise Exception('Failed to advance to Pre Doc')
        
def set_pre_doc(driver, pre_doc_dict):
    pre_doc = PreDoc(driver)
 
    pre_doc.set_bank_code(pre_doc_dict['bank_code'])
    pre_doc.set_branch_num(pre_doc_dict['branch_num'])
    pre_doc.set_account_num(pre_doc_dict['account_num'])
    pre_doc.set_gov_bank_code(pre_doc_dict['gov_bank_code'])
    pre_doc.set_gov_branch_num(pre_doc_dict['gov_branch_num'])
    pre_doc.set_observation(pre_doc_dict['observation'])
    
def check_pre_doc(driver, pre_doc_dict):
    pre_doc = PreDoc(driver)
    
    right = True

    right = right and pre_doc.check_bank_code(pre_doc_dict['bank_code'])
    right = right and pre_doc.check_branch_num(pre_doc_dict['branch_num'])
    right = right and pre_doc.check_account_num(pre_doc_dict['account_num'])
    right = right and pre_doc.check_gov_bank_code(pre_doc_dict['gov_bank_code'])
    right = right and pre_doc.check_gov_branch_num(pre_doc_dict['gov_branch_num'])
    right = right and pre_doc.check_observation(pre_doc_dict['observation'])

    if right:
        print('Pre Doc tab values match their expected values')
        return 
    else:
        raise Exception('Pre Doc tab values do not match their expected value')    
        
def confirm_pre_doc(driver):
    pre_doc = PreDoc(driver)
    
    pre_doc.click_confirm_btn()
    
    if pre_doc.is_predoc_confirmed():
        print('Confirmed Pre Doc creation')
        return
    else:
        raise Exception('Failed to confirm Pre Doc creation')
        
def from_pre_doc_to_cost_center(driver):
    pre_doc = PreDoc(driver)
    
    pre_doc.click_cost_center()
    
    if pre_doc.advanced_to_cost_center():
        print('Advanced to Cost Center Tab')
    else:
        raise Exception('Failed to advance to Cost Center Tab')
    
def set_cost_center(driver, cc_dict):
    cost_center = CostCenter(driver)

    cost_center.click_first_row_checkbox()
    cost_center.set_month(cc_dict['month'])
    cost_center.set_year(cc_dict['year'])    
    
def check_cost_center(driver, cc_dict):
    cost_center = CostCenter(driver)
    
    right = True
    
    right = right and cost_center.check_month(cc_dict['month'])
    right = right and cost_center.check_year(cc_dict['year'])
    
    if right:
        print('Cost Center tab values match their expected values')
        return 
    else:
        raise Exception('Cost Center tab values do not match their expected value')     
    
def confirm_cost_center(driver, cc_dict):
    cost_center = CostCenter(driver)
    
    cost_center.click_confirm()
    
    if cost_center.check_total_cost(cc_dict['value']):
        print('Cost Center tab total cost is correct')
    else:
        raise Exception('Failed to input the correct total cost in Cost Center tab')
        
def register_dh(driver):
    register = Register(driver)
    
    register.click_register_dh()
    
    if register.advanced_to_registered_panel():
        print('Advanced to registered DH panel')
        return
    else:
        raise Exception('Failed to advance to registered DH panel')
    
def get_dh(driver):
    register = Register(driver)
    
    raw_string = register.extract_string_in_class_legend()
    dh = register.check_string_in_class_legend(raw_string)
    
    return dh

def return_from_dh_panel(driver):
    register = Register(driver)
    register.click_return_btn()
    
    if register.returned_to_incdh():
        print('Returned to INCDH')
        return
    else:
        raise Exception('Failed to return to INCDH') 