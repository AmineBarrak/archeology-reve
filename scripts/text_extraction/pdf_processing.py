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
import fitz
from PIL import Image


def clean_text(rgx_match, text):
    
    new_text = re.sub(rgx_match, '', text)
    return new_text


def count_rotated_text_percentage(text, nbr_caracter_moyen):
	text = space_remove(text)
	regex_rotated = '\n([a-zÀ-ÿ]{1,4}[[[[:space:]][a-zÀ-ÿ]{1,3}]?[[[:space:]][a-zÀ-ÿ]{1,3}]?]?)'

	exactMatch = re.compile(regex_rotated, flags=re.IGNORECASE)
	match_bad = len(exactMatch.findall(text))/nbr_caracter_moyen
	text = clean_text(regex_rotated, text)
	word_list = text.split()
	total_of_words = len(word_list)



	return match_bad/total_of_words



def images_extraction(pdf_path, folder_save):
	# pip install pymupdf
	# open the file
	pdf_file = fitz.open(pdf_path)
	  
	# STEP 3
	# iterate over PDF pages
	for page_index in range(len(pdf_file)):
	    
	    # get the page itself
	    page = pdf_file[page_index]
	   
	    for image_index, img in enumerate(page.getImageList(), start=1):
	        
	        # get the XREF of the image
	        xref = img[0]
	          
	        # extract the image bytes
	        base_image = pdf_file.extractImage(xref)
	        # get the image extension
	        image_ext = base_image["ext"]
	        
	        
	        image_bytes = base_image["image"]
	        image = Image.open(io.BytesIO(image_bytes))
	        try:
	        	image.save(folder_save+str(page_index)+"_"+str(image_index)+"."+image_ext)
	        except:
	        	print("An exception occurred")
	        


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

def remove_weird_characters(text):
	text=re.sub(r'.*�.*\n',  r'', text)

	return text

def remove_one_char_line(text):
	text =re.sub(r'\n.?\n',  r'\n', text)
	return text


def text_preprocessing(text, output_file):
	# with open(input_file) as f:
	# 	text = f.read()
	
	# ~ add cleaning functions
	text = space_remove(text)


	text = fix_rotated_text(text)
	text = link_lines(text)
	
	text = remove_empty_lines(text)
	text = link_dashed_word(text)
	text = remove_weird_characters(text)
	text = remove_one_char_line(text)
	
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
    

def tika(filename, file_path):
	print("*********** Converting the file {} *******************".format(filename))
	parsedPDF = parser.from_file(file_path)

	return parsedPDF['content']
	# with open(save_path, 'w') as f:
	# 	f.write(parsedPDF['content'])
	
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
	PATH="../../dataset/straight/"
	RES_PATH="../../extracted_text/"
	files_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.pdf']
	


	for file_path in files_paths:
		filename = Path(file_path).stem
		# print(filename)
		file_extract_path = RES_PATH+filename
		Path(file_extract_path).mkdir(parents=True, exist_ok=True)

		text_extracted = tika(filename, file_path)
		text_preprocessing(text_extracted, file_extract_path+"/"+filename+".txt")

		folder_save_image = file_extract_path+"/images/"
		Path(folder_save_image).mkdir(parents=True, exist_ok=True)
		images_extraction(file_path, folder_save_image)



def count_loss_percentages():
	PATH="../../dataset/straight/"
	RES_PATH="../../extracted_text/"
	files_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.pdf']
	
	nbr_caracter_moyen_usage = 5.13
	nbr_caracter_moyen_dict = 10.09

	nbr_total_files = len (files_paths)
	percentage_usage = 0
	percentage_dict = 0
	for file_path in files_paths:
		filename = Path(file_path).stem
		# print(filename)
		file_extract_path = RES_PATH+filename
		Path(file_extract_path).mkdir(parents=True, exist_ok=True)

		text_extracted = tika(filename, file_path)

		percentage_usage += count_rotated_text_percentage(text_extracted, nbr_caracter_moyen_usage)
		percentage_dict += count_rotated_text_percentage(text_extracted, nbr_caracter_moyen_dict)

	print("*********** Loss words usage {:.2f} *******************".format((percentage_usage/nbr_total_files)*100))
	print("*********** Loss words dictionnaire {:.2f} *******************".format((percentage_dict/nbr_total_files)*100))

if __name__ == '__main__':
	main()
	# count_loss_percentages()

	






	
  
