# -*- coding: utf-8 -*-
import os
import glob

# 366, 371, 372 feita

SRC_FOLDER = 'C:\\Users\\Tales\\Desktop\\graviola\\src'
#SRC_FOLDER = os.path.dirname(__file__)
GRAV_FOLDER = os.path.dirname(SRC_FOLDER)
APS_FOLDER = GRAV_FOLDER + os.sep + 'aps'

def get_pdf_files():
    pdf_files = [pdf for pdf in glob.glob(APS_FOLDER + os.sep + '*.pdf')]
    return pdf_files

##############################################################################

from pdfminer.high_level import extract_text

pdf_files = get_pdf_files()

one_file = pdf_files[0]
two_file = pdf_files[1]

text1 = extract_text(one_file)
text2 = extract_text(two_file)

with open('text2.txt', 'w') as f:
    f.write(text2)

list_of_strings = text.split(sep = '\n\n')

# get more examples and see if they are consistent. they are not

list_of_strings[0] # total_value
list_of_strings[1]
list_of_strings[2] # data da AP
list_of_strings[3] # cpf. nem sempre
list_of_strings[4] # conta-corrente
list_of_strings[5] #
list_of_strings[6]
list_of_strings[7]
list_of_strings[8] # total_value
list_of_strings[9]
list_of_strings[10]
list_of_strings[11] # número da ap
list_of_strings[12]
list_of_strings[13]
list_of_strings[14]
list_of_strings[15]
list_of_strings[16]
list_of_strings[17]
list_of_strings[18]
list_of_strings[19]
list_of_strings[20]
list_of_strings[21]
list_of_strings[22] # processo
list_of_strings[23]
list_of_strings[24] # nome favorecido. nem sempre
list_of_strings[25] # nome do banco às vezes
list_of_strings[26] # bank name. às vezes favorecido
list_of_strings[27] # agencia
list_of_strings[28]
list_of_strings[29] # observacao
list_of_strings[30]
list_of_strings[31]
list_of_strings[32] # número do empenho e subelemento
list_of_strings[33]
list_of_strings[34]
list_of_strings[35]
list_of_strings[36]
list_of_strings[37]
list_of_strings[38]
list_of_strings[39]
list_of_strings[40]
list_of_strings[41]
list_of_strings[42]
list_of_strings[43]
list_of_strings[44]
list_of_strings[45]
list_of_strings[46]
list_of_strings[47]
list_of_strings[48]
list_of_strings[49]
list_of_strings[50]
list_of_strings[51]
list_of_strings[52]
list_of_strings[53]
list_of_strings[54]
list_of_strings[55]
list_of_strings[56]
list_of_strings[57]
list_of_strings[58]
list_of_strings[59]
list_of_strings[60]