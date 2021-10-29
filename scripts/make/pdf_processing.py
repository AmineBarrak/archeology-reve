import segmentation.py
import PyPDF2
import pdfplumber
from pdfminer.pdfpage import PDFPage
import os
from tika import parser
import pytesseract
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
from pathlib import Path
import io
from pdf2image import convert_from_path
import easyocr
import numpy as np
import PIL
from PIL import ImageDraw
import spacy
import regex as re



def fix_rotated_text(text):
	
	
	text=re.sub(r'\n(?|(au)|(et)|(de)|(des))([[[:space:]][a-zÀ-ÿ]{2,4}]?)\n',  r' \1\2 ', text)
	text=re.sub(r'\n([a-zÀ-ÿ]{1})\n',  r'\1 ', text)
	text=re.sub(r'\n([a-zÀ-ÿ]{1,4}[[[[:space:]][a-zÀ-ÿ]{1,3}]?[[[:space:]][a-zÀ-ÿ]{1,3}]?]?)',  r'\1', text)
	text=re.sub(r'\n([a-zÀ-ÿ]{1,7}[[[:space:]][a-zÀ-ÿ]{1,7}]?[[[:space:]][a-zÀ-ÿ]{1,7}]?)',  r'\1', text)
	text=re.sub(r'\n([a-zÀ-ÿ]{1,7}[[[:space:]][a-zÀ-ÿ]{1,7}]?[[[:space:]][a-zÀ-ÿ]{1,7}]?)',  r'\1', text)

	return text

def link_dashed_word(text):
	text=re.sub(r'(\w)\n- (\w)',  r'\1\2', text)
	text=re.sub(r'(\w)- (\w)',  r'\1\2', text)
	return text
	
def remove_empty_lines(text):
	text=re.sub(r'\n(-|\.)[[:space:]]*\d+',  r'', text)
	text=re.sub(r'\n[[:space:]]*\d+',  r'', text)
	return text

def link_lines(text):
	text=re.sub(r'\n([a-zÀ-ÿ])',  r' \1', text)
	
	return text

def space_remove(text):
	text=re.sub(r'(\s)+',  r'\1', text)
	return text



def text_preprocessing(input_file, output_file):
	with open(input_file) as f:
		text = f.read()
	
	# ~ add cleaning functions
	text = space_remove(text)
	text = fix_rotated_text(text)
	text = link_lines(text)
	
	text = remove_empty_lines(text)
	text = link_dashed_word(text)
	
	# ~ for line in text.splitlines():
		# ~ print(line)
	
	with open(output_file, 'w') as f:
		f.write(text)
		



def write_results (row, out):
	with open(out, "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerow(row)
		

		
def pdfminer(filename, file_path, save_path):
	resource_manager = PDFResourceManager()
	fake_file_handle = io.StringIO()
	converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
	page_interpreter = PDFPageInterpreter(resource_manager, converter)

	with open(file_path, 'rb') as fh:

		for page in PDFPage.get_pages(fh,
									  caching=True,
									  check_extractable=True):
			page_interpreter.process_page(page)

		text = fake_file_handle.getvalue()

	# close open handles
	converter.close()
	fake_file_handle.close()
	
	with open(save_path, 'w') as f:
		f.write(text)
    

def tika(filename, file_path, save_path):
	print("*********** Converting the file {} *******************".format(filename))
	parsedPDF = parser.from_file(file_path)
	with open(save_path, 'w') as f:
		f.write(parsedPDF['content'])
	
def pdfplumber(filename, file_path, save_path):
	with pdfplumber.open(file_path) as pdf:
		
		for page in pdf.pages:
			with open(save_path, 'w') as f:
				f.write(page.extract_text())


def OCR(filename, file_path, save_path):
	# ~ ! apt-get install poppler-utils
	# ~ ! pip install easyocr pdf2image
	
	reader = easyocr.Reader(['fr'])
	images = convert_from_path(file_path)
	
	text = ""
	for i in range(len(images)):
	  bound = reader.readtext(np.array(images[i]))
	  for j in range(len(bound)):
		  text = bound[j][1]+'\n'
		  with open(save_path, "a") as f:
			  f.write(text)
	  
	


	

def pypdf2(filename, file_path, save_path):
	pdf_file = open(file_path, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdf_file)
	count = pdfReader.numPages
	for i in range(count):
		page = pdfReader.getPage(i)
		with open(save_path, 'w') as f:
			f.write(page.extract_text())



  
def main():
	# ~ PATH="../../dataset/straight/"
	# ~ RES_PATH="../../dataset/text_extraction/"
	# ~ files_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.pdf']
	
	# print(len(file_paths))


	# ~ for file_path in files_paths:
		# ~ filename = Path(file_path).stem
		# print(filename)
	# ~ tika(filename, file_path, RES_PATH+filename+".txt")
	filename = "GuideDéveloppementDurable_BasseRésolution-2013.txt"
	# ~ tika(filename, filename, "res.txt")
	
	text_preprocessing(filename, "res2.txt")
	
	
if __name__ == '__main__':
	main()
	
  
