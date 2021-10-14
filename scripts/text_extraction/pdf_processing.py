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
import io
from pathlib import Path



def write_results (row, out):
	with open(out, "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerow(row)
		
def pdfminer(filename, file_name, save_path):
	resource_manager = PDFResourceManager()
	fake_file_handle = io.StringIO()
	converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
	page_interpreter = PDFPageInterpreter(resource_manager, converter)

	with open(file_name, 'rb') as fh:

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
    

def tika(filename, file_name, save_path):
	print("*********** Converting the file {} *******************".format(filename))
	parsedPDF = parser.from_file(file_name)
	with open(save_path, 'w') as f:
		f.write(parsedPDF['content'])
	
def pdfplumber(filename, file_name, save_path):
	with pdfplumber.open(file_name) as pdf:
		
		for page in pdf.pages:
			with open(save_path, 'w') as f:
				f.write(page.extract_text())


def pypdf2(filename, file_name, save_path):
	pdf_file = open(file_name, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdf_file)
	count = pdfReader.numPages
	for i in range(count):
		page = pdfReader.getPage(i)
		with open(save_path, 'w') as f:
			f.write(page.extract_text())



  
def main():
	PATH="../../dataset/straight/"
	RES_PATH="../../dataset/text_extraction/"
	file_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.pdf']
	
	# print(len(file_paths))


	for file in file_paths:
		filename = Path(file).stem
		# print(filename)

		tika(filename, file, RES_PATH+filename+".txt")
	
if __name__ == '__main__':
	main()
	
  
