
# STEP 1
# import libraries
import fitz
import io
from PIL import Image


# STEP 2
# file path you want to extract images from
file = "test.pdf"
  
# open the file
pdf_file = fitz.open(file)
  
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
        image.save(str(page_index)+"_"+str(image_index)+"."+image_ext)
