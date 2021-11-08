# -*- coding: utf-8 -*-
import unittest
from os import chdir, path, sep

test_folder = path.dirname(__file__)
root_folder = path.dirname(test_folder)
chdir(root_folder + sep + 'src')

from from_pdf_to_string import StringProcessor

#==============================================================================

class StringGetterTest(unittest.TestCase):
    pass
    # only a call to pdfminer.high_level.extract_text. no need to test it
    
class StringProcessorTest(unittest.TestCase):
    # assumes only ' ' shows up. not built to deal with \f and other characters as such
    def test_returns_unchanged_string_when_there_are_no_spaces_at_all(self):
        test_string = 'ABCDEFGHIJKL12356'
        processor = StringProcessor()
        output = processor.squeeze_multiple_spaces(test_string)
        self.assertEqual(output, 'ABCDEFGHIJKL12356')
    
    def test_returns_unchanged_string_when_there_are_only_single_spaces_in_the_middle_of_the_input(self):
        test_string = 'A B C D E FGHIJKL12356'
        processor = StringProcessor()
        output = processor.squeeze_multiple_spaces(test_string)
        self.assertEqual(output, 'A B C D E FGHIJKL12356')
        
    def test_removes_initial_and_trailing_spaces(self):
        test_string = ' A B C D E FGHIJKL12356 '
        processor = StringProcessor()
        output = processor.squeeze_multiple_spaces(test_string)
        self.assertEqual(output, 'A B C D E FGHIJKL12356')
    
    def test_squeezes_multiple_spaces(self):
        test_string = '  A  B  C  D  '
        processor = StringProcessor()
        output = processor.squeeze_multiple_spaces(test_string)
        self.assertEqual(output, 'A B C D')
        
    def test_process_removes_newlines_and_squeezes_spaces(self):
        test_string = '  A \n B \n C  D  \n'
        processor = StringProcessor()
        output = processor.process(test_string)
        self.assertEqual(output, 'A B C D')
    
if __name__ == '__main__':
    unittest.main()

