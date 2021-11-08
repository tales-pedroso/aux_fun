# -*- coding: utf-8 -*-

from pdfminer.high_level import extract_text

def get_processed_string_from_pdf(pdf_filepath):
    pipeline = Pipeline(StringGetter, StringProcessor)
    processed_string = pipeline.pipeline(pdf_filepath)
    return processed_string

class StringGetter():
    def get(self, pdf_filepath):
        string = extract_text(pdf_filepath)
        return string

class StringProcessor():
    def remove_newlines(self, string):
        no_newlines = string.replace('\n', ' ')
        return no_newlines
    
    def squeeze_multiple_spaces(self, string):
        no_spaces = ' '.join(string.split())
        return no_spaces
    
    def process(self, string):
        no_newlines = self.remove_newlines(string)
        no_multiple_spaces = self.squeeze_multiple_spaces(no_newlines)
        return no_multiple_spaces
    
class Pipeline():
    def __init__(self, string_getter, string_processor):
        self.string_getter = string_getter()
        self.string_processor = string_processor()
        
    def pipeline(self, pdf_filepath):
        raw_string = self.string_getter.get(pdf_filepath)
        processed_string = self.string_processor.process(raw_string)
        return processed_string