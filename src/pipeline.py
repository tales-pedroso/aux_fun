# -*- coding: utf-8 -*-
from re import search, sub, VERBOSE, UNICODE

#==============================================================================
class Getter(): 
    def get_text_between(self, this, that, raw_string):
        pattern = f'''{this}(.*?){that}'''
        match = search(pattern, raw_string, VERBOSE)
        
        if match is None:
            return None
        
        text = match.groups()[0]
        return text
    
    def get_next_n_chars(self, substring, string, n):
        start_index = string.find(substring)
        next_n_chars = string[start_index:start_index + n + 1]
        
        return next_n_chars
    
    def get_previous_n_chars(self, substring, string, n):
        stop_index = string.find(substring)
        
        if stop_index == -1:
            return None
        
        string_up_to_substring = string[:stop_index]
        previous_n_chars = string_up_to_substring[-n:]
        
        return previous_n_chars
        
class ValueGetter(Getter):     
    def get(self, raw_string):
        start = 'IMPORTÂNCIA\sA\sPAGAR:\sR\$'
        finish = '\('
        
        text = self.get_text_between(start, finish, raw_string)
        return text
    
class NeGetter(Getter):
    def get(self, raw_string):
        start = 'EMPENHO'
        finish = 'ELEM.\sDE\sDESPESA'
        
        text = self.get_text_between(start, finish, raw_string)
        return text
    
class ApGetter(Getter):
    def get(self, raw_string):
        start = 'AP\snº\s'       # starting with 'AP nº '
        finish = '(?<=/\d{4})\s' # look-behind assertion for '/0000' for any digit then a space
        
        text = self.get_text_between(start, finish, raw_string)
        return text
    
class ProcessNumGetter(Getter):
    def get(self, raw_string):
        start = 'EXPEDIENTE'       
        finish = 'FAVORECIDO' 
        
        text = self.get_text_between(start, finish, raw_string)
        return text
    
class BranchNumGetter(Getter):
    def get(self, raw_string):
        ten_chars_before_historico = self.get_previous_n_chars(' HISTÓRICO', raw_string, 10)
        
        return ten_chars_before_historico
    
class SubelementNumGetter(Getter):
    def get(self, raw_string):
        start = 'ELEM\.\sDE\sDESPESA'
        finish = 'ITEM\sDE\sPROG'
        
        text = self.get_text_between(start, finish, raw_string)
        return text
    
class ObservationGetter(Getter):
    def get(self, raw_string):
        start = 'Autorizo\so\spagamento\sdo' 
        finish = 'Certidão\sde\sÓbito'
        
        text = self.get_text_between(start, finish, raw_string)
        return text

class DeceasedPersonNameGetter(Getter):
    def get(self, observation):
        start = 'Auxílio\sFuneral'
        finish = 'CPF'
        
        text = self.get_text_between(start, finish, observation)
        return text
    
class DateOfDeathGetter(Getter):
    def get(self, observation):
        start = 'falecid'
        finish = ','
        
        text = self.get_text_between(start, finish, observation)
        return text
    
class CpfGetter(Getter):
    def get(self, raw_string):
        start = 'CPF\s'
        finish = '\s'
        
        text = self.get_text_between(start, finish, raw_string)
        
        if text is None:
            return None
        else:
            text_plus_next_50_chars = self.get_next_n_chars(text, raw_string, 50) # 30 chars would be enough
            return text_plus_next_50_chars
        
class AccountNumGetter(Getter):
    def get(self, raw_string):
        twenty_chars_before_vencimento = self.get_previous_n_chars(' VENCIMENTO', raw_string, 20)
        
        return twenty_chars_before_vencimento
    
class ApDateGetter(Getter):
    def get(self, raw_string):
        start = 'DATA:\s'
        finish = '(?<=\d{2}/\d{2}/\d{4})\s'
        
        text = self.get_text_between(start, finish, raw_string)
        return text
        
class BankNameGetter(Getter):
    def get(self, raw_string):
        # probably not the most efficient way. try a map implementation and test both them both
        start = 'BANCO:\s'
        list_of_finishes = ['(?<=BANCO\sDO\sBRASIL)', 
                            '(?<=ITAÚ)',
                            '(?<=CAIXA\sECONÔMICA\sFEDERAL)']
        
        list_of_results = [self.get_text_between(start, finish, raw_string) for finish in list_of_finishes]
        
        result = [result for result in list_of_results if result is not None]
        
        if len(result) == 0:
            return None
        else:
            return result.pop()
    
#==============================================================================
class Processor():
    def strip(self, text):
        stripped_text = text.strip()
        return stripped_text
    
    def remove_all_spaces(self, text):
        no_spaces = text.replace(' ', '')
        return no_spaces
    
    def remove_dots(self, text):
        no_dots = text.replace('.', '')
        return no_dots
    
    def remove_hyphen(self, text):
        no_hyphen = text.replace('-', '')
        return no_hyphen
    
    def remove_commas(self, text):
        no_commas = text.replace(',', '')
        return no_commas
    
    def truncate_to_first_n_chars(self, text, n):
        if text is None:
            return None
        
        first_n_chars = text[:n]
        return first_n_chars
    
    def zfill_until_4_chars(self, text):
        zfilled = text.zfill(4)
        return zfilled
    
    def get_last_n_digits(self, text, n):
        last_n_digits = text[-n:]
        return last_n_digits
    
    def remove_lowercase_letter(self, text):
        # it does not test accents used in polish names, only common accents used in brazilian names
        no_lowercase = sub('[a-zà-ÿ]', '', text, UNICODE)
        return no_lowercase
        
    def get_date(self, text):
        # doesn't test if date is invalid number, e.g. 06/15/2021
        pattern = '(\d{2}[/\.]\d{2}[/\.]\d{4})' 
        match = search(pattern, text, VERBOSE)
        
        if match is None:
            return None
        
        processed_text = match.groups()[0]
        return processed_text
    
    def change_dots_into_slashes(self, text):
        from_dots_to_slashes = sub('\.', '/', text)
        return from_dots_to_slashes
    
    def get_last_part(self, text):
        split_text = text.split(' ')
        last_part = split_text[-1]
        return last_part
    
    def process(self, text):
        # default behavior of processors. if a class needs something different, it overrides this
        return self.strip(text)

class BranchNumProcessor(Processor):
    def process(self, text):
        last_part = self.get_last_part(text)
        no_spaces = self.remove_all_spaces(last_part)
        no_dots = self.remove_dots(no_spaces)
        no_hyphen = self.remove_hyphen(no_dots)
        
        if len(no_hyphen) > 6:
            return None
        elif len(no_hyphen) == 6:
            no_hyphen = no_hyphen[1:]
        
        first_4_chars = self.truncate_to_first_n_chars(no_hyphen, 4)
        zfilled = self.zfill_until_4_chars(first_4_chars)
        return zfilled

class SubelementNumProcessor(Processor):
    def process(self, text):
        no_spaces = self.remove_all_spaces(text)
        last_2_digits = self.get_last_n_digits(no_spaces, 2)
        return last_2_digits

class DeceasedPersonNameProcessor(Processor):
    def process(self, text):
        only_uppercase_letters = self.remove_lowercase_letter(text)
        no_commas = self.remove_commas(only_uppercase_letters)
        no_hyphen = self.remove_hyphen(no_commas)
        stripped_text = self.strip(no_hyphen)
        return stripped_text
    
class DateOfDeathProcessor(Processor):
    def process(self, text):
        date_of_death = self.get_date(text)
        
        if date_of_death is None:
            return None
        
        from_dots_to_slashes = self.change_dots_into_slashes(date_of_death)
        return from_dots_to_slashes
    
class CpfProcessor(Processor):
    def process(self, text):
        first_14_chars = self.truncate_to_first_n_chars(text, 14)
        return first_14_chars
    
class AccountNumProcessor(Processor):
    def process(self, text):
        no_trailing_spaces = text.rstrip()
        
        account_num = no_trailing_spaces.split(' ')[-1]
        
        no_hyphen = self.remove_hyphen(account_num)
        no_dots = self.remove_dots(no_hyphen)
        return no_dots
    
#==============================================================================
class Checker():
    def has_pattern(self, pattern, processed_text):
        match = search(pattern, processed_text, VERBOSE)
        has_pattern = match is not None
        
        return has_pattern
    
    def has_letters(self, processed_text):
        pattern = '[a-zA-Z]'
        has_letters = self.has_pattern(pattern, processed_text)
        
        return has_letters
    
    def has_only_digits_commas_and_dots(self, processed_text):
        pattern = '[^\d\.,]'
        has_only_digits_commas_and_dots = not self.has_pattern(pattern, processed_text)
        
        return has_only_digits_commas_and_dots
    
    def get_next_n_chars(self, chunk, whole_string, n):
        start_index = whole_string.find(chunk)
        next_n_chars = whole_string[start_index:start_index + n + 1]
        
        return next_n_chars
    
    def ends_in(self, string, char):
        ends_in = string[-1] == char
        return ends_in
    
class ValueChecker(Checker):
    def check(self, processed_text):
        pattern = '.*\d,\d\d$' # ",99" but not ",99 "
        is_valid = self.has_pattern(pattern, processed_text)
        
        is_valid = is_valid and self.has_only_digits_commas_and_dots(processed_text)
        
        return is_valid
    
class NeChecker(Checker):
    def check(self, processed_text):
        pattern = '^\d{4}NE\d{6}$'
        is_valid = self.has_pattern(pattern, processed_text)
        
        return is_valid
    
class ApChecker(Checker):
    def check(self, processed_text):
        pattern = '^\d{1,4}/\d{4}$'
        is_valid = self.has_pattern(pattern, processed_text)
        
        return is_valid
    
class ProcessNumChecker(Checker):
    def check(self, processed_text):
        pattern = '''^\d{7}     # 7 digits   0045142
                      \.\d{8}   # .8 digits  .00001057
                      /         # slash      /
                      \d{4}     # 4 digits   2021         
                      -         # hyphen     -
                      \d{2}$    # 2 digits   05
                      '''
        is_valid = self.has_pattern(pattern, processed_text)
        
        return is_valid
    
class BranchNumChecker(Checker):
    def check(self, processed_text):
        if len(processed_text) != 4:
            return False
        
        pattern = '''\d{4}|          # either 4 digits
                     \d{3}[xX]       # or 3 digits and a x, whatever the case
                     ''' 
        
        is_valid = self.has_pattern(pattern, processed_text)
        
        return is_valid
    
class SubelementNumChecker(Checker):
    def check(self, processed_text):
        if len(processed_text) != 2:
            return False
        
        pattern = '\d{2}'
        
        is_valid = self.has_pattern(pattern, processed_text)
        
        return is_valid
    
class DeceasedPersonNameChecker(Checker):
    def check(self, processed_text):
        # check if the person has at least one surname
        list_of_names = processed_text.split(' ')
        
        if len(list_of_names) < 2:
            return False
        else:
            return True
    
class DateOfDeathChecker(Checker):
    def check(self, processed_text):
        pattern = '\d{2}/\d{2}/\d{4}'
        
        is_valid = self.has_pattern(pattern, processed_text)
        return is_valid
    
class CpfFirstChecker(Checker):
    def check(self, text):
        if 'SIAPE' in text:
            return False
        else:
            return True
        
class CpfSecondChecker(Checker):
    def check(self, processed_text):
        pattern = '^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        
        is_valid = self.has_pattern(pattern, processed_text)
        return is_valid
    
class AccountNumChecker(Checker):
    def check(self, processed_text):
        last_char = processed_text[-1]
        
        valid_last_chars = [str(i) for i in range(0, 10)]
        valid_last_chars.extend(['x', 'X', 'p', 'P'])
        
        if last_char not in valid_last_chars:
            return False
        
        # since last_char is okay, let's test if the rest is number
        rest = processed_text[:-1]
        
        pattern = '^\d{1,19}$'
        
        is_valid = self.has_pattern(pattern, rest)
        return is_valid
        
class ApDateChecker(Checker):
    def check(self, processed_text):
        pattern = '^\d{2}/\d{2}/\d{4}$'
        is_valid = self.has_pattern(pattern, processed_text)
        return is_valid
    
class BankNameChecker(Checker):
    def check(self, processed_text):
        valid_names = {'BANCO DO BRASIL', 'ITAÚ', 'CAIXA ECONÔMICA FEDERAL'}
        is_valid = processed_text in valid_names
        
        return is_valid
    
#=============================================================================
class Pipeline():
    def __init__(self, getter, processor, checker):
        self.getter = getter()
        self.processor = processor()
        self.checker = checker()
    
    def pipeline(self, raw_string):
        text = self.getter.get(raw_string)
        
        if text is None: # avoid sending None to the next stage even if it is impossible
            return None
        
        processed_text = self.processor.process(text) 
        
        if processed_text is None: # avoid sending None to the next stage even if it is impossible
            return None
        
        is_valid = self.checker.check(processed_text)       
        
        if is_valid:
            return processed_text
        else:
            return None
        
class DoubleGetterPipeline():
    def __init__(self, outer_getter, inner_getter, processor, checker):
        self.outer_getter = outer_getter()
        self.inner_getter = inner_getter()
        self.processor = processor()
        self.checker = checker()
        
    def pipeline(self, raw_string):
        outer_text = self.outer_getter.get(raw_string)
        
        if outer_text is None: # avoid sending None to the next stage even if it is impossible
            return None
        
        inner_text = self.inner_getter.get(outer_text)
        
        if inner_text is None: # avoid sending None to the next stage even if it is impossible
            return None
        
        processed_text = self.processor.process(inner_text) 
        
        if processed_text is None: # avoid sending None to the next stage even if it is impossible
            return None
        
        is_valid = self.checker.check(processed_text)       
        
        if is_valid:
            return processed_text
        else:
            return None
        
class DoubleCheckerPipeline():
    def __init__(self, getter, first_checker, processor, second_checker):
        self.getter = getter()
        self.first_checker = first_checker()
        self.processor = processor()
        self.second_checker = second_checker()
        
    def pipeline(self, raw_string):
        text = self.getter.get(raw_string)
        
        if text is None: # avoid sending None to the next stage even if it is impossible
            return None
        
        is_valid = self.first_checker.check(text)
        
        if not is_valid:
            return None
        
        processed_text = self.processor.process(text) 
        
        if processed_text is None: # avoid sending None to the next stage even if it is impossible
            return None
        
        is_valid = self.second_checker.check(processed_text)       
        
        if is_valid:
            return processed_text
        else:
            return None

class ValuePipeline(Pipeline):
    def __init__(self):
        super().__init__(ValueGetter, Processor, ValueChecker)
        
class NePipeline(Pipeline):
    def __init__(self):
        super().__init__(NeGetter, Processor, NeChecker)
        
class ApPipeline(Pipeline):
    def __init__(self):
        super().__init__(ApGetter, Processor, ApChecker)
        
class ProcessNumPipeline(Pipeline):
    def __init__(self):
        super().__init__(ProcessNumGetter, Processor, ProcessNumChecker)
        
class BranchNumPipeline(Pipeline):
    def __init__(self):
        super().__init__(BranchNumGetter, BranchNumProcessor, BranchNumChecker)
        
class SubelementNumPipeline(Pipeline):
    def __init__(self):
        super().__init__(SubelementNumGetter, SubelementNumProcessor, SubelementNumChecker)

class DeceasedPersonNamePipeline(DoubleGetterPipeline):
    def __init__(self):
        super().__init__(ObservationGetter, DeceasedPersonNameGetter, DeceasedPersonNameProcessor, DeceasedPersonNameChecker)
        
class DateOfDeathPipeline(DoubleGetterPipeline):
    def __init__(self):
        super().__init__(ObservationGetter, DateOfDeathGetter, DateOfDeathProcessor, DateOfDeathChecker)
        
class CpfPipeline(DoubleCheckerPipeline):
    def __init__(self):
        super().__init__(CpfGetter, CpfFirstChecker, CpfProcessor, CpfSecondChecker)
        
class AccountNumPipeline(Pipeline):
    def __init__(self):
        super().__init__(AccountNumGetter, AccountNumProcessor, AccountNumChecker)
        
class ApDatePipeline(Pipeline):
    def __init__(self):
        super().__init__(ApDateGetter, Processor, ApDateChecker)
        
class BankNamePipeline(Pipeline):
    def __init__(self):
        super().__init__(BankNameGetter, Processor, BankNameChecker)