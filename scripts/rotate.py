#!/usr/bin/env python3

import PyPDF2
import sys
import os




def rotate(pdf_path_imput, pdf_path_output, list_pages):
    pdfIn = open(pdf_path_imput, 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfIn)
    pdfWriter = PyPDF2.PdfFileWriter()
    for pageNum in range(pdfReader.numPages):
        page = pdfReader.getPage(pageNum)
        if pageNum in list_pages:
            page.rotateClockwise(90)
        pdfWriter.addPage(page)

    pdfOut = open(pdf_path_output, 'wb')
    pdfWriter.write(pdfOut)
    pdfOut.close()
    pdfIn.close()

def main():
    folder_path="/home/amine/Documents/darine_project/archeology-reve/dataset/straight/pdf_text"
    os.chdir(folder_path)
    list_pages = sys.argv[3].split(',')
    list_pages = ([int(x) for x in list_pages])
    print(list_pages)
    rotate(sys.argv[1], sys.argv[2] ,list_pages)
if __name__ == '__main__':
    main()