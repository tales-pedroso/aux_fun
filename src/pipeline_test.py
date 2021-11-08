# -*- coding: utf-8 -*-

#SRC_FOLDER = 'C:\\Users\\Tales\\Desktop\\graviola\\src'
import unittest

from pipeline import (Getter, ValueGetter, NeGetter, ApGetter, ProcessNumGetter, BranchNumGetter, 
                      SubelementNumGetter, ObservationGetter, DeceasedPersonNameGetter, DateOfDeathGetter, 
                      CpfGetter, AccountNumGetter,
                      Processor, BranchNumProcessor, SubelementNumProcessor, DeceasedPersonNameProcessor, 
                      DateOfDeathProcessor, CpfProcessor, AccountNumProcessor,
                      Checker, ValueChecker, NeChecker, ApChecker, ProcessNumChecker, BranchNumChecker, 
                      SubelementNumChecker, DeceasedPersonNameChecker, DateOfDeathChecker, CpfFirstChecker, 
                      CpfSecondChecker, AccountNumChecker,
                      ValuePipeline, NePipeline, ApPipeline, ProcessNumPipeline, BranchNumPipeline, 
                      SubelementNumPipeline, DeceasedPersonNamePipeline, DateOfDeathPipeline, CpfPipeline,
                      AccountNumPipeline)

class GetterTest(unittest.TestCase):
    def test_gets_the_shortest_string_when_ambiguous(self):
        test_string = 'start get_this1 finish get_this2 finish get this3'
        getter = Getter()
        output = getter.get_text_between('start', 'finish', test_string)
        self.assertEqual(output, ' get_this1 ')
        
    def test_gets_text_when_pattern_matches(self):
        test_string = 'start get_this finish'
        getter = Getter()
        output = getter.get_text_between('start', 'finish', test_string)
        self.assertEqual(output, ' get_this ')
    
    def test_gets_none_when_pattern_doesnt_match(self):
        test_string = 'start get_this finish'
        getter = Getter()
        output = getter.get_text_between('start', 'finish0', test_string)
        self.assertEqual(output, None)
        
    def test_gets_none_when_arg_is_empty_string(self):
        test_string = ''
        getter = Getter()
        output = getter.get_text_between('start', 'finish0', test_string)
        self.assertEqual(output, None)
        
    def test_gets_next_char_when_n_is_1(self): 
        test_string = '0123456789'
        getter = Getter()
        output = getter.get_next_n_chars('0', test_string, 1)
        self.assertEqual(output, '01')
        
    def test_gets_next_2_chars_when_n_is_2(self): 
        test_string = '0123456789'
        getter = Getter()
        output = getter.get_next_n_chars('0', test_string, 2)
        self.assertEqual(output, '012')
        
    def test_gets_the_rest_of_the_string_when_n_is_larger_than_the_length_of_the_string(self): 
        test_string = '0123456789'
        getter = Getter()
        output = getter.get_next_n_chars('0', test_string, 1000)
        self.assertEqual(output, '0123456789')
        
    def test_gets_whole_initial_string_when_n_is_larger_than_the_input(self):
        test_string = 'abcdefghijklmnopqrstuv'
        getter = Getter()
        output = getter.get_previous_n_chars('kl', test_string, 50)
        self.assertEqual(output, 'abcdefghij')
        
    def test_gets_previous_chars_when_n_is_small(self):
        test_string = 'abcdefghijklmnopqrstuv'
        getter = Getter()
        output = getter.get_previous_n_chars('v', test_string, 2)
        self.assertEqual(output, 'tu')
        
    def test_gets_none_when_substring_is_not_present_in_string(self):
        test_string = 'abcdefghijklmnopqrstuv'
        getter = Getter()
        output = getter.get_previous_n_chars('z', test_string, 5)
        self.assertEqual(output, None)
    
class ValueGetterTest(unittest.TestCase):
    def test_gets_value_when_pattern_matches(self):
        test_string = 'IMPORTÂNCIA A PAGAR: R$ 1.347,55 (mil trezentos ...)'
        getter = ValueGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' 1.347,55 ')
    
    def test_gets_none_when_pattern_doesnt_match(self):
        test_string = 'IMPORTÂNCIA A PAGAR R$ 1.347,55 (mil trezentos ...)' # without :
        getter = ValueGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
    def test_gets_value_when_there_is_no_space_before(self):
        test_string = 'IMPORTÂNCIA A PAGAR: R$1.347,55 (mil trezentos ...)'
        getter = ValueGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '1.347,55 ')
        
    def test_gets_value_when_there_is_no_space_after(self):
        test_string = 'IMPORTÂNCIA A PAGAR: R$ 1.347,55(mil trezentos ...)'
        getter = ValueGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' 1.347,55')
        
class NeGetterTest(unittest.TestCase):
    def test_gets_value_when_pattern_matches(self):
        test_string = 'EMPENHO 2021NE000029 ELEM. DE DESPESA 33.'
        getter = NeGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' 2021NE000029 ')
    
    def test_gets_none_when_pattern_doesnt_match(self):
        test_string = 'EMPENHO 2021NE000029 ELEMENTO DE DESPESA 33.' # doesn't end in ELEM.
        getter = NeGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
        
class ApGetterTest(unittest.TestCase):
    def test_gets_value_when_pattern_matches(self):
        test_string = 'ESTATÍSTICA AP nº 374/2021 AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '374/2021')
    
    def test_gets_the_shortest_string_when_ambiguous(self):
        test_string = 'ESTATÍSTICA AP nº 374/2021 AUTORIZAÇÃO DE PAGAMENTO 999/9999'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '374/2021')
    
    def test_gets_none_when_spacing_is_violated(self):
        test_string = 'ESTATÍSTICA AP nº 374/2021AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
        
    def test_gets_clean_number_when_there_are_2_spaces(self):
        test_string = 'ESTATÍSTICA AP nº 1/2021  AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '1/2021')
        
    def test_gets_number_when_input_is_1_digit_long(self):
        test_string = 'ESTATÍSTICA AP nº 1/2021 AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '1/2021')
    
    def test_gets_number_when_input_is_2_digits_long(self):
        test_string = 'ESTATÍSTICA AP nº 01/2021 AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '01/2021')
    
    def test_gets_number_when_input_is_3_digits_long(self):
        test_string = 'ESTATÍSTICA AP nº 001/2021 AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '001/2021')
    
    def test_gets_number_when_input_is_4_digits_long(self):
        test_string = 'ESTATÍSTICA AP nº 0001/2021 AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '0001/2021')
        
    def test_gets_string_even_when_input_has_letters(self):
        test_string = 'ESTATÍSTICA AP nº aB1/2021 AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, 'aB1/2021')
    
    def test_gets_none_if_year_is_2_digits_long(self):
        test_string = 'ESTATÍSTICA AP nº 001/21 AUTORIZAÇÃO DE'
        getter = ApGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
class ProcessNumGetterTest(unittest.TestCase):
    def test_gets_text_when_input_is_right(self):
        test_string = 'Nº DO PROC/EXPEDIENTE 0045142.00001057/2021-07 FAVORECIDO MARIA'
        getter = ProcessNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' 0045142.00001057/2021-07 ')
    
    def test_gets_text_when_there_is_no_space_before(self):
        test_string = 'Nº DO PROC/EXPEDIENTE0045142.00001057/2021-07 FAVORECIDO MARIA'
        getter = ProcessNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '0045142.00001057/2021-07 ')
    
    def test_gets_text_when_there_is_no_space_after(self):
        test_string = 'Nº DO PROC/EXPEDIENTE 0045142.00001057/2021-07FAVORECIDO MARIA'
        getter = ProcessNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' 0045142.00001057/2021-07')
    
    def test_gets_none_if_pattern_doesnt_match(self):
        test_string = 'Nº DO PROC/EXPEDIENTe 0045142.00001057/2021-07 FAVORECIDO MARIA'
        getter = ProcessNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
        
class BranchNumGetterTest(unittest.TestCase):
    def test_gets_num_when_input_is_right(self):
        test_string = 'BANCO DO BRASIL 1826 HISTÓRICO'
        getter = BranchNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '1826 ')
    
    def test_gets_none_when_there_is_no_historico_keyword(self):
        test_string = 'BANCO DO BRASIL 1826 HISTORICO' # missing acute accent
        getter = BranchNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
        
    def test_gets_whatever_comes_before_historico_keyword(self):
        test_string = 'random text 1.8/2*6y HISTÓRICO'  # people do type . when the expected input is a number
        getter = BranchNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '1.8/2*6y ')
        
class SubelementNumGetterTest(unittest.TestCase):
    def test_gets_num_when_start_is_elem_de_despesa_and_finish_is_item_de_prog(self):
        test_string = '2021NE000029 ELEM. DE DESPESA 3390.08-03 ITEM DE PROG: FO'
        getter = SubelementNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' 3390.08-03 ')
        
    def test_gets_num_when_input_starts_without_space(self):
        test_string = '2021NE000029 ELEM. DE DESPESA3390.08-03 ITEM DE PROG: FO'
        getter = SubelementNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '3390.08-03 ')
    
    def test_gets_num_when_input_ends_without_space(self):
        test_string = '2021NE000029 ELEM. DE DESPESA 3390.08-03ITEM DE PROG: FO'
        getter = SubelementNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' 3390.08-03')
    
    def test_gets_none_when_start_isnt_elem_de_despesa(self):
        test_string = '2021NE000029 ELEMENTO DE DESPESA 3390.08-03 ITEM DE PROG: FO' # ELEMENTO instead of ELEM.
        getter = SubelementNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
    def test_gets_none_when_finish_isnt_item_de_prog(self):
        test_string = '2021NE000029 ELEM. DE DESPESA 3390.08-03 ITEM DE PROE' # PROE instead of PROG:
        getter = SubelementNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
class ObservationGetterTest(unittest.TestCase):
    def test_gets_observation_when_start_is_right_and_finish_is_right(self):
        test_string = 'sometext sometext Autorizo o pagamento do Auxílio Funeral do ex-servidor HELIO GEORGINO DA SILVA , CPF 353.304.227-87 , SIAPE 764178 , falecido em 11/09/2021 , conforme Certidão de Óbito nº 051'
        getter = ObservationGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' Auxílio Funeral do ex-servidor HELIO GEORGINO DA SILVA , CPF 353.304.227-87 , SIAPE 764178 , falecido em 11/09/2021 , conforme ')
    
    def test_gets_none_when_start_is_missing(self):
        test_string = 'pagamento do Auxílio Funeral da ex-servidora ROSA DULCE DE MARA VIANNA MOTTA , CPF 212.285.587-87  '
        getter = ObservationGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
    def test_gets_none_when_finish_is_missing(self):
        test_string = 'Autorizo o pagamento do Auxílio Funeral do ex-servidor HELIO GEORGINO DA SILVA , CPF 353.304.227-87 , SIAPE 764178 , falecido em 11/09/2021 , conforme Atestado de Óbito' # changed text
        getter = ObservationGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
class DeceasedPersonNameGetterTest(unittest.TestCase):
    def test_gets_name_when_start_is_right_and_finish_is_right(self):
        test_string = 'some_text Auxílio Funeral do ex-servidor HELIO GEORGINO DA SILVA , CPF 231.'
        getter = DeceasedPersonNameGetter()
        output = getter.get(test_string)
        self.assertEqual(output, ' do ex-servidor HELIO GEORGINO DA SILVA , ')
    
    def test_gets_none_when_start_is_missing(self):
        test_string = 'Funeral do ex-servidor HELIO GEORGINO DA SILVA , CPF 231.'
        getter = DeceasedPersonNameGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
    def test_gets_none_when_finish_is_missing(self):
        test_string = 'Auxílio Funeral do ex-servidor HELIO GEORGINO DA SILVA , 231.958.262-53'
        getter = DeceasedPersonNameGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
        
class DateOfDeathGetterTest(unittest.TestCase):
    def test_gets_date_when_start_is_right_and_finish_is_right(self):
        test_string = '54 , falecido em 13/10/2021 , co'
        getter = DateOfDeathGetter()
        output = getter.get(test_string)
        self.assertEqual(output, 'o em 13/10/2021 ')
        
    def test_gets_date_when_feminine_article_is_used(self):
        test_string = '54 , falecida em 13/10/2021 , co'
        getter = DateOfDeathGetter()
        output = getter.get(test_string)
        self.assertEqual(output, 'a em 13/10/2021 ')
    
    def test_gets_none_when_start_is_missing(self):
        test_string = '54 , morreu em 13/10/2021 , co'
        getter = DateOfDeathGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
    def test_gets_none_when_finish_is_missing(self):
        test_string = '54 , falecida em 13/10/2021 conforme'
        getter = DateOfDeathGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
    def test_gets_date_when_year_is_2_digits(self):
        test_string = '54 , falecido em 13/10/21 , co'
        getter = DateOfDeathGetter()
        output = getter.get(test_string)
        self.assertEqual(output, 'o em 13/10/21 ')
    
    def test_gets_date_when_dot_is_separator(self):
        test_string = '54 , falecido em 13.10.2021 , co'
        getter = DateOfDeathGetter()
        output = getter.get(test_string)
        self.assertEqual(output, 'o em 13.10.2021 ')
        
class CpfGetterTest(unittest.TestCase):
    def test_gets_text_when_start_is_cpf_and_finish_is_space(self):
        test_string = 'CPF 111.222.333-44 , SIAPE 000000 , falecido em 11/09/2021'
        getter = CpfGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '111.222.333-44 , SIAPE 000000 , falecido em 11/09/2')
    
    def test_gets_none_when_start_is_not_uppercase_cpf(self):
        test_string = 'bla cPF 111.111.222-33 bla'
        getter = CpfGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
    def test_gets_none_when_finish_is_not_space(self):
        test_string = 'bla CPF 111.111.222-33bla'
        getter = CpfGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
    def test_gets_first_cpf_when_there_are_2_of_them_more_than_50_chars_apart(self):
        test_string = 'bla CPF 111.111.111-11 bla1 bla2 bla3 bla4 bla5 bla6 bla7 bla8 bla9 bla10 bla bla bla bla CPF 000.000.000-00'
        getter = CpfGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '111.111.111-11 bla1 bla2 bla3 bla4 bla5 bla6 bla7 b')
        
class AccountNumGetterTest(unittest.TestCase):
    def test_gets_account_num_when_input_is_more_than_20_chars_long(self):
        test_string = 'CPF 222.111.657-91 18.863-8 VENCIMENTO'
        getter = AccountNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '.111.657-91 18.863-8')
        
    def test_gets_account_num_when_input_has_two_spaces_before_vencimento(self):
        test_string = 'CPF 222.111.657-91 18.863-8  VENCIMENTO'
        getter = AccountNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, '111.657-91 18.863-8 ')
        
    def test_gets_account_num_when_input_is_less_than_20_chars_long(self):
        test_string = 'aaa 18.863-8 VENCIMENTO'
        getter = AccountNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, 'aaa 18.863-8')
    
    def test_gets_none_when_finish_is_not_vencimento(self):
        test_string = '.657-91 18.863-8 vENCIMENTO'
        getter = AccountNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
        
    def test_gets_none_when_finish_is_not_spacevencimento(self):
        test_string = '.657-91 18.863-8VENCIMENTO'
        getter = AccountNumGetter()
        output = getter.get(test_string)
        self.assertEqual(output, None)
    
#==============================================================================

class ProcessorTest(unittest.TestCase):
    # probably overkill, since these are just calls to regular str methods
    def test_strip_spaces_in_string(self):
        test_string = ' abc '
        processor = Processor()
        output = processor.strip(test_string)
        self.assertEqual(output, 'abc')
    
    def test_remove_dots_in_string(self):
        test_string = ' ab.c '
        processor = Processor()
        output = processor.remove_dots(test_string)
        self.assertEqual(output, ' abc ')
    
    def test_remove_hyphen_in_string(self):
        test_string = '-_-'
        processor = Processor()
        output = processor.remove_hyphen(test_string)
        self.assertEqual(output, '_')
    
    def test_truncate_string_to_first_4_chars(self):
        test_string = '12345678'
        processor = Processor()
        output = processor.truncate_to_first_n_chars(test_string, 4)
        self.assertEqual(output, '1234')
        
    def test_gets_uppercase_name_without_spaces(self):
        test_string = 'TALES'
        processor = Processor()
        output = processor.remove_lowercase_letter(test_string)
        self.assertEqual(output, 'TALES')
    
    def test_gets_uppercase_name_with_spaces(self):
        test_string = 'TALES DE ASSIS'
        processor = Processor()
        output = processor.remove_lowercase_letter(test_string)
        self.assertEqual(output, 'TALES DE ASSIS')
    
    def test_gets_uppercase_name_with_acute_accent(self): 
        test_string = ' ÁÉÍÓÚ '
        processor = Processor()
        output = processor.remove_lowercase_letter(test_string)
        self.assertEqual(output, ' ÁÉÍÓÚ ')
    
    def test_gets_uppercase_name_with_apostrofe(self):
        test_string = "TALES D'ASSIS"
        processor = Processor()
        output = processor.remove_lowercase_letter(test_string)
        self.assertEqual(output, "TALES D'ASSIS")
    
    def test_gets_uppercase_name_with_tilde(self):
        test_string = 'ÃÕÑ'
        processor = Processor()
        output = processor.remove_lowercase_letter(test_string)
        self.assertEqual(output, 'ÃÕÑ')
        
    def test_gets_uppercase_name_with_circumflex_accent(self):
        test_string = 'ÂÊÎÔÛ'
        processor = Processor()
        output = processor.remove_lowercase_letter(test_string)
        self.assertEqual(output, 'ÂÊÎÔÛ')
    
class BranchNumProcessorTest(unittest.TestCase):
    def test_gets_clean_branch_num_when_input_is_already_clean(self):
        test_string = '6317'
        processor = BranchNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '6317')
        
    def test_gets_clean_branch_num_when_input_has_spaces(self):
        test_string = ' 631 7 '
        processor = BranchNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '6317')
    
    def test_gets_clean_branch_num_when_input_has_hyphen(self):
        test_string = '6317-2'
        processor = BranchNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '6317')
        
    def test_gets_clean_branch_num_when_input_has_dots(self):
        test_string = '6.317-2'
        processor = BranchNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '6317')
    
    def test_gets_clean_branch_num_when_input_has_confirmation_digit_without_hyphen(self):
        test_string = '63172'
        processor = BranchNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '6317')
        
    def test_gets_leading_zeros_if_input_has_leading_zeros(self):
        test_string = '06317'
        processor = BranchNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '0631')
        
    def test_fills_with_zeros_if_input_has_less_than_4_chars(self):
        test_string = '1'
        processor = BranchNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '0001')
        
    def test_returns_unchanged_if_input_has_4_chars(self):
        test_string = '6317'
        processor = BranchNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '6317')
    
class SubelementNumProcessorTest(unittest.TestCase):
    def test_gets_number_when_string_ends_in_space(self):
        test_string = '3390.08-03 '
        processor = SubelementNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '03')
        
    def test_gets_number_when_string_doesnt_end_in_space(self):
        test_string = '3390.08-03'
        processor = SubelementNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '03')
    
class DeceasedPersonNameProcessorTest(unittest.TestCase):
    def test_gets_name_when_input_is_right(self):
        test_string = ' do ex-servidor ROBERTO RAPOSO DA SILVA FILHO , '
        processor = DeceasedPersonNameProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, 'ROBERTO RAPOSO DA SILVA FILHO')
        
    def test_gets_name_when_input_is_right_with_female_name(self):
        test_string = ' da ex-servidora MARIA EDWIRGENS DE LIMA , '
        processor = DeceasedPersonNameProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, 'MARIA EDWIRGENS DE LIMA')
        
    def test_gets_name_with_apostrophes(self):
        test_string = " da ex-servidora ROSANA D'ALMA SAGRADA, "
        processor = DeceasedPersonNameProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, "ROSANA D'ALMA SAGRADA")
        
    def test_gets_name_with_accents(self):
        test_string = " da ex-servidora MÁÉÍÓÚÃÀÑ ÂÊÎÔÛ , "
        processor = DeceasedPersonNameProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, 'MÁÉÍÓÚÃÀÑ ÂÊÎÔÛ')
        
    def test_gets_name_when_input_does_not_have_commas(self):
        test_string = " do ex-servidor ROBERTO RAPOSO DA SILVA FILHO "
        processor = DeceasedPersonNameProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, 'ROBERTO RAPOSO DA SILVA FILHO')
        
    def test_gets_name_when_input_does_not_have_leading_or_trailing_spaces(self):
        test_string = "do ex-servidor ROBERTO RAPOSO DA SILVA FILHO"
        processor = DeceasedPersonNameProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, 'ROBERTO RAPOSO DA SILVA FILHO')
        
    def test_gets_name_when_input_has_dots(self):
        test_string = "do ex-servidor FULANO DA SILVA JR."
        processor = DeceasedPersonNameProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, 'FULANO DA SILVA JR.')
        
class DateOfDeathProcessorTest(unittest.TestCase):
    def test_gets_date_when_person_is_male(self):
        test_string = 'o em 13/10/2021 '
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '13/10/2021')
    
    def test_gets_date_when_person_is_female(self):
        test_string = 'a em 13/10/2021 '
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '13/10/2021')
    
    def test_gets_date_when_separator_is_forward_slash(self):
        test_string = 'a em 09/02/2019 '
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '09/02/2019')
    
    def test_gets_date_when_separator_is_dot(self):
        test_string = 'a em 09.02.2019 '
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '09/02/2019')
    
    def test_gets_none_when_year_is_two_digits_long(self):
        test_string = 'a em 09/02/21 '
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, None)
    
    def test_gets_date_when_year_is_four_digits_long(self):
        test_string = 'a em 09/02/2021 '
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '09/02/2021')
    
    def test_gets_date_when_there_are_no_leading_spaces(self):
        test_string = 'o em13/10/2021 '
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '13/10/2021')
    
    def test_gets_date_when_there_are_no_trailing_spaces(self):
        test_string = 'o em 13/10/2021'
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '13/10/2021')
        
    def test_gets_none_when_input_has_letter(self):
        test_string = 'o em q3/10/2021' # simulating a typo
        processor = DateOfDeathProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, None)
    
class CpfProcessorTest(unittest.TestCase):
    def test_gets_cpf_when_input_is_right(self):
        test_string = '111.222.333-44 18.863-8 VENCIMENTO R$ 2.508,37 bla bla'
        processor = CpfProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '111.222.333-44')
    
    def test_gets_none_when_input_is_none(self):
        test_string = None
        processor = CpfProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, None)
        
class AccountNumProcessorTest(unittest.TestCase):
    def test_gets_clean_account_num_when_input_is_only_numbers(self):
        test_string = '12345678901234567890'
        processor = AccountNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '12345678901234567890')
        
    def test_gets_clean_account_num_when_input_mix_other_numbers(self):
        test_string = '.111.657-91 18.863-8'
        processor = AccountNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '188638')
        
    def test_gets_clean_account_num_when_input_mix_numbers_and_letters(self):
        test_string = ' CORRENTE: 878190710'
        processor = AccountNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '878190710')
    
    def test_gets_clean_account_num_when_input_has_hyphen(self):
        test_string = ' CORRENTE: 8781907-0'
        processor = AccountNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '87819070')
    
    def test_gets_clean_account_num_when_input_has_dots(self):
        test_string = '.111.657-91 18.863-8'
        processor = AccountNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '188638')
    
    def test_gets_clean_account_num_when_input_has_letter(self):
        test_string = '12345678px'
        processor = AccountNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '12345678px')
        
    def test_gets_clean_account_num_when_input_ends_in_space(self):
        test_string = '.111.657-91 18.863-8  ' 
        processor = AccountNumProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, '188638')
    
#==============================================================================    
    
class CheckerTest(unittest.TestCase):
    def test_has_pattern_returns_true_when_pattern_matches(self):
        test_string = 'start get_this finish'
        pattern = 'get_this'
        checker = Checker()
        output = checker.has_pattern(pattern, test_string)
        self.assertEqual(output, True)
    
    def test_has_pattern_returns_false_when_pattern_doesnt_match(self):
        test_string = 'start get_this finish'
        pattern = 'get this'
        checker = Checker()
        output = checker.has_pattern(pattern, test_string)
        self.assertEqual(output, False)
    
    def test_has_letters_returns_true_when_string_has_lowercase_letter(self):
        test_string = '999 t 765$#@'
        checker = Checker()
        output = checker.has_letters(test_string)
        self.assertEqual(output, True)
    
    def test_has_letters_returns_true_when_string_has_uppercase_letter(self):
        test_string = '999 T 765$#@'
        checker = Checker()
        output = checker.has_letters(test_string)
        self.assertEqual(output, True)
    
    def test_returns_false_when_string_does_not_have_letters(self):
        test_string = '999 ! 765$#@'
        checker = Checker()
        output = checker.has_letters(test_string)
        self.assertEqual(output, False)
    
    def test_returns_true_when_string_has_only_digits_commas_and_dots(self):
        test_string = '836.312,99.1.0.1,,'
        checker = Checker()
        output = checker.has_only_digits_commas_and_dots(test_string)
        self.assertEqual(output, True)
    
    def test_returns_false_when_string_has_space(self):
        test_string = '8.36,11 283'
        checker = Checker()
        output = checker.has_only_digits_commas_and_dots(test_string)
        self.assertEqual(output, False)
        
    def test_returns_false_when_string_has_other_symbols(self):
        test_string = '8.36,11/283'
        checker = Checker()
        output = checker.has_only_digits_commas_and_dots(test_string)
        self.assertEqual(output, False)
    
class ValueCheckerTest(unittest.TestCase):
    def test_returns_true_when_string_ends_in_comma_digit_digit(self):
        test_string = '65342,88'
        checker = ValueChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
        
    def test_returns_false_when_string_ends_in_comma_digit_digit_digit(self):
        test_string = '65342,888'
        checker = ValueChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_string_ends_in_space(self):
        test_string = '65342,88 '
        checker = ValueChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_true_when_string_has_dots(self):
        test_string = '65.342,88'
        checker = ValueChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_true_for_large_string(self):
        test_string = '1.701.997.365.342,88'
        checker = ValueChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
class NeCheckerTest(unittest.TestCase):
    def test_returns_false_when_string_ends_in_space(self):
        test_string = '2021NE379201 '
        checker = NeChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_string_starts_in_space(self):
        test_string = ' 2021NE379201'
        checker = NeChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_pattern_doesnt_match(self):
        test_string = '2021NP379201'
        checker = NeChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_true_when_pattern_matches(self):
        test_string = '2021NE000001'
        checker = NeChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
class ApCheckerTest(unittest.TestCase):
    def test_returns_false_when_string_starts_in_space(self):
        test_string = ' 300/2017'
        checker = ApChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_string_ends_in_space(self):
        test_string = '300/2017 '
        checker = ApChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_true_when_number_is_1_digit_long(self):
        test_string = '1/2020'
        checker = ApChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_true_when_number_is_4_digits_long(self):
        test_string = '9876/5432'
        checker = ApChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_false_when_number_is_5_digits_long(self):
        test_string = '00001/2021'
        checker = ApChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_string_has_letters(self):
        test_string = 'abc1/2021'
        checker = ApChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
class ProcessNumCheckerTest(unittest.TestCase):
    def test_returns_true_when_input_is_right(self):
        test_string = '0045142.00001057/2021-07'
        checker = ProcessNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_false_when_input_is_longer_than_expected(self):
        test_string = '00045142.00001057/2021-07' # one more zero
        checker = ProcessNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_input_is_shorter_than_expected(self):
        test_string = '0045142.0001057/2021-07' # one less zero
        checker = ProcessNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_if_there_is_letters(self):
        test_string = 'p045142.00001057/2021-07' # leading 'p'
        checker = ProcessNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_if_string_starts_with_space(self):
        test_string = ' 0045142.00001057/2021-07' 
        checker = ProcessNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_if_string_ends_in_space(self):
        test_string = '0045142.00001057/2021-07 ' 
        checker = ProcessNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)

class BranchNumCheckerTest(unittest.TestCase):
    def test_returns_true_when_input_is_4_digits(self):
        test_string = '9999'
        checker = BranchNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_false_when_input_is_less_than_4_digits(self):
        test_string = '999'
        checker = BranchNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_input_is_more_than_4_digits(self):
        test_string = '99991'
        checker = BranchNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_true_when_input_has_letter_x(self):
        test_string = '999x'
        checker = BranchNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_false_when_input_has_any_other_letter_than_x(self):
        test_string = '999p'
        checker = BranchNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_input_has_hyphen(self):
        test_string = '99-2'
        checker = BranchNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_input_has_space(self):
        test_string = '99 2'
        checker = BranchNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
class SubelementNumCheckerTest(unittest.TestCase):
    def test_returns_false_when_there_are_letters(self):
        test_string = '9a'
        checker = SubelementNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_false_when_input_is_more_than_2_digits_long(self):
        test_string = '967'
        checker = SubelementNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_false_when_input_is_less_than_2_digits_long(self):
        test_string = ''
        checker = SubelementNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_false_when_string_has_hyphen(self):
        test_string = '-3'
        checker = SubelementNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_false_when_string_has_dots(self):
        test_string = '.9'
        checker = SubelementNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_true_when_input_is_2_digits(self):
        test_string = '36'
        checker = SubelementNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
class DeceasedPersonNameCheckerTest(unittest.TestCase):
    def test_returns_true_if_person_has_2_names(self):
        test_string = 'Tales Pedroso'
        checker = DeceasedPersonNameChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_true_if_person_has_a_lot_of_names(self):
        test_string = 'Pedro de Alcântara Francisco Antônio João Carlos Xavier de Paula Miguel Rafael Joaquim José Gonzaga Pascoal Cipriano Serafim de Bragança e Bourbon'
        checker = DeceasedPersonNameChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_false_if_person_has_only_one_name(self):
        test_string = 'Mário'
        checker = DeceasedPersonNameChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_true_if_name_is_a_1_letter_word(self):
        test_string = 'Serafim da Costa e Filho'
        checker = DeceasedPersonNameChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_true_if_name_is_a_long_word(self):
        test_string = 'Anticonstitucionalissimamente da Silva'
        checker = DeceasedPersonNameChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
class DateOfDeathCheckerTest(unittest.TestCase):
    def test_returns_true_when_input_is_a_valid_date(self):
        test_string = '05/02/2021'
        checker = DateOfDeathChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
        
    def test_returns_true_when_input_is_a_future_date(self):
        test_string = '05/02/9999'
        checker = DateOfDeathChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_true_when_input_is_a_past_date(self):
        test_string = '05/02/0000'
        checker = DateOfDeathChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_true_when_input_is_an_invalid_date(self):
        test_string = '99/99/9999'
        checker = DateOfDeathChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_false_when_input_has_letters(self):
        test_string = '13/08/q999'
        checker = DateOfDeathChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_year_is_2_digits(self):
        test_string = '27/02/21'
        checker = DateOfDeathChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
class CpfFirstCheckerTest(unittest.TestCase):
    def test_returns_false_when_siape_keyword_is_present(self):
        test_string = 'CPF 111.111.111-11, SIAPE 000000 , falecido em 11/09/2'
        checker = CpfFirstChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_true_when_siape_keyword_is_absent(self):
        test_string = 'CPF 111.111.111-11, SIAPe 000000 , falecido em 11/09/2'
        checker = CpfFirstChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
class CpfSecondCheckerTest(unittest.TestCase):
    def test_returns_true_when_string_follows_cpf_structure(self):
        test_string = '369.128.438-83'
        checker = CpfSecondChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_false_when_there_are_leading_spaces(self):
        test_string = ' 369.128.438-83'
        checker = CpfSecondChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_false_when_there_are_trailing_spaces(self):
        test_string = '369.128.438-83 '
        checker = CpfSecondChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_it_does_not_have_the_first_dot(self):
        test_string = '369128.438-83'
        checker = CpfSecondChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_false_when_it_does_not_have_the_second_dot(self):
        test_string = '369.128438-83'
        checker = CpfSecondChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_it_does_not_have_hyphen(self):
        test_string = '369.128.43883'
        checker = CpfSecondChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_it_has_forward_slash(self):
        test_string = '369.128.438/83'
        checker = CpfSecondChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_it_is_not_started_by_3_numbers(self):
        # some people omit leading zeros
        test_string = '00.128.438-83'
        checker = CpfSecondChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
class AccountNumCheckerTest(unittest.TestCase):
    def test_returns_true_when_input_is_only_number(self):
        test_string = '0123456789'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
        
    def test_returns_true_when_input_ends_in_x(self):
        test_string = '0123456789x'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
        
    def test_returns_true_when_input_ends_in_p(self):
        test_string = '0123456789p'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
    
    def test_returns_false_when_input_ends_in_letter_other_than_x_or_p(self):
        test_string = '01234673l'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_false_when_input_has_letter_in_other_position_than_the_end(self):
        test_string = '01234673x0'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_input_has_hyphen(self):
        test_string = '1234-5'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_input_has_slash(self):
        test_string = '1234/5'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_input_has_dots(self):
        test_string = '12345.6'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
    
    def test_returns_false_when_input_has_space(self):
        test_string = '1234 5'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_false_when_input_is_only_1_digit(self):
        test_string = '3'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)
        
    def test_returns_true_when_input_is_2_digits_long(self):
        test_string = '12'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
        
    def test_returns_true_when_input_is_20_digits_long(self):
        test_string = '12345678901234567890'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertTrue(output)
        
    def test_returns_false_when_input_is_more_than_20_digits_long(self):
        test_string = '123456789012345678901'
        checker = AccountNumChecker()
        output = checker.check(test_string)
        self.assertFalse(output)

#==============================================================================
    
class PipelineTest(unittest.TestCase):
    pass
    # just instantiates other classes and check for Nones along the way 
    # no need to test it
    
class ValuePipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_correct(self):
        test_string = 'IMPORTÂNCIA A PAGAR: R$ 5.674,75(cinco mil, seiscentos e setenta e quatro reais e sete'
        pipeline = ValuePipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, '5.674,75')
    
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'IMPORTÂNCIA A PAGAR: R$ 5a674,75 (cinco mil, seiscentos e setenta e quatro reais e sete'
        pipeline = ValuePipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, None)
        
class NePipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_correct(self):
        test_string = 'TOTAL Nº DO EMPENHO 2021NE000029 ELEM. DE DESPESA 3390.08-03 ITEM DE PROG:'
        pipeline = NePipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, '2021NE000029')
        
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'TOTAL Nº DO EMPENHO 2021NE0000129 ELEM. DE DESPESA 3390.08-03 ITEM DE PROG:' # 7 numbers instead of 6
        ne_pipeline = NePipeline()
        output = ne_pipeline.pipeline(test_string)
        self.assertEqual(output, None)
        
class ApPipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_correct(self):
        test_string = 'some_text AP nº 394/2021 AUTORIZAÇÃO some_more_text'
        pipeline = ApPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, '394/2021')
        
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'some_text E ESTATÍSTICA APs nº 394/2021 AUTORIZAÇÃO some_more_text' # extra 's'
        pipeline = ApPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, None)
        
class ProcessNumPipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_correct(self):
        test_string = 'CONTA CORRENTE: Nº DO PROC/EXPEDIENTE 0045142.00001057/2021-07 FAVORECIDO MARIA'
        pipeline = ProcessNumPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, '0045142.00001057/2021-07')
    
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'CONTA CORRENTE: Nº DO PROC/EXPEDIENTE 0045142.00001057/2021-07 FaVORECIDO MARIA' # lowercase 'a'
        pipeline = ProcessNumPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, None)
    
class BranchNumPipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_correct(self):
        test_string = 'BANCO: BANCO DO BRASIL 1826 HISTÓRICO'
        branch_num_pipeline = BranchNumPipeline()
        output = branch_num_pipeline.pipeline(test_string)
        self.assertEqual(output, '1826')
    
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'BANCO: BANCO DO BRASIL 182e HISTÓRICO'
        pipeline = BranchNumPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, None)
    
class SubelementNumPipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_right(self):
        test_string = 'ELEM. DE DESPESA 3390.08-03 ITEM DE PROG: F' 
        subelement_num_pipeline = SubelementNumPipeline()
        output = subelement_num_pipeline.pipeline(test_string)
        self.assertEqual(output, '03')
    
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'ELEM. DE DESPESA 3390.08-03 ITEN DE PROG: F' # typo in ITEM
        pipeline = SubelementNumPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, None)
        
class DeceasedPersonNamePipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_right(self):
        test_string = 'Autorizo o pagamento do Auxílio Funeral do ex-servidor inativo TOMAZ JOSÉ DE SOUZA, CPF 111.111.111-11 , SIAPE 000000 , falecido em 14/09/2021 , conforme Certidão de Óbito nº'
        pipeline = DeceasedPersonNamePipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, 'TOMAZ JOSÉ DE SOUZA')
    
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'Autorizo o pagamento do Auxílio Funeral do ex-servidor inativo TOMAZ , CPF 111.111.111-11 , SIAPE 000000, falecido em 14/09/2021 , conforme Certidão de Óbito nº'
        deceased_person_name_pipeline = DeceasedPersonNamePipeline()
        output = deceased_person_name_pipeline.pipeline(test_string)
        self.assertEqual(output, None)
    
class DateOfDeathPipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_right(self):
        test_string = 'Autorizo o pagamento do Auxílio Funeral do ex-servidor inativo TOMAZ JOSÉ DE SOUZA, CPF 111.111.111-11 , SIAPE 000000 , falecido em 14/09/2021 , conforme Certidão de Óbito nº'
        pipeline = DateOfDeathPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, '14/09/2021')
        
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'Autorizo o pagamento do Auxílio Funeral do ex-servidor inativo TOMAZ JOSÉ DE SOUZA, CPF 111.111.111-11 , SIAPE 000000, falecido em 14/09/21 , conforme Certidão de Óbito nº'
        pipeline = DateOfDeathPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, None)
        
class CpfPipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_right(self):
        test_string = '24/09/2021 CPF 369.128.438-83 18.863-8 VENCIMENTO R$ 2.508,37'
        pipeline = CpfPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, '369.128.438-83')
    
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'A , CPF 353.304.227-87 , SIAPE 764178 , falecido em 11/09/2021 , conforme Cer'
        pipeline = CpfPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, None)
        
class AccountNumPipelineTest(unittest.TestCase):
    def test_returns_correct_value_when_input_is_right(self):
        test_string = 'CPF 222.222.222-22 11.318-2 VENCIMENTO'
        pipeline = AccountNumPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, '113182')
        
    def test_returns_correct_value_when_input_is_right2(self):
        # there are a few pdfs that exibit this pattern of input
        test_string = 'CORRENTE: 878.907-0 VENCIMENTO'
        pipeline = AccountNumPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, '8789070')
    
    def test_returns_none_when_input_is_wrong(self):
        test_string = 'CPF 222.222.222-22 11.3a8-2 VENCIMENTO' 
        pipeline = AccountNumPipeline()
        output = pipeline.pipeline(test_string)
        self.assertEqual(output, None)

if __name__ == '__main__':
    unittest.main()
    


