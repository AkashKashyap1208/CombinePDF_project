import os
import shutil
import json
import pprint
import PyPDF2  #pip install 'PyPDF2<3.0' 
from PyPDF2 import PdfReader, PdfFileWriter

# Directory containing the PDF files
pdf_directory = '/home/aakash/Documents/Combine_Pdf_Project/'

# Initialize a list to store the PDF files
ALL_PDF_LIST = []

# Iterate through files in the directory
for filename in os.listdir(pdf_directory + 'ALL_PDF') :
    if filename.endswith('.pdf'):
        # Split the filename into parts using underscores
        parts = filename.split('_')
        
        # Extract the relevant information from the filename
        file_info = {
            'id': parts[0],
            'PersonName': parts[1],
            'type': parts[2],
            'date': parts[3].split('.')[0],
            'time': parts[3].split('.')[1],  # Remove the ".pdf" extension
            'OriginalFileName': filename                 
        }
        
        # Append the file_info dictionary to the list
        ALL_PDF_LIST.append(file_info)

# Initialize a dictionary to group items by 'id'
items_by_id = {}

# Iterate over the items in ALL_PDF_LIST and group them by 'id'
for item in ALL_PDF_LIST:
  item_id = item["id"]
  if item_id not in items_by_id:
    items_by_id[item_id] = []
  items_by_id[item_id].append(item)


# Initialize the final_list
final_list = []
final_list_2 = []



# Iterate over the items_by_id dictionary
for key, value in items_by_id.items():
  print(" value = ",value)


  
  if len(value)>1:
        output_pdf = PdfFileWriter()
        finalFileName = value[0]['id'] + '_' + value[0]['PersonName'] + '_final_'
        finalDate = ''
        finalTime = ''
      
        file_types = set()
        for key, singleFile in enumerate(value):
           file_name = singleFile["OriginalFileName"]
           finalDate += ("" if key == 0 else "_") + singleFile['date']
           finalTime += '_' + singleFile['time']

           # Open the PDF files
           pdf_stream = PdfReader(open(pdf_directory + 'ALL_PDF/' + file_name, 'rb'))

           # Ensure the output directory exists
           os.makedirs(pdf_directory + 'FINAL_COMBINED_PDF', exist_ok=True)


           # Add pages from the first PDF
           for page_num in range(pdf_stream.getNumPages()):
             page = pdf_stream.getPage(page_num)
             output_pdf.addPage(page)

        finalFileName = finalFileName + finalDate + finalTime + '.pdf'

        print("Final File Name ",finalFileName)

        with open(os.path.join(pdf_directory, 'FINAL_COMBINED_PDF', finalFileName), 'wb') as output_file:
            output_pdf.write(output_file)

  else:
    singleFile = value[0]
    file_name = singleFile["OriginalFileName"]
    
    # Ensure the output directory exists
    os.makedirs(os.path.join(pdf_directory, 'FINAL_COMBINED_PDF'), exist_ok=True)
    
    # Copy the single PDF file to the FINAL_COMBINED_PDF directory
    source_path = os.path.join(pdf_directory, 'ALL_PDF', file_name)
    destination_path = os.path.join(pdf_directory, 'FINAL_COMBINED_PDF', file_name)
    
    shutil.copy(source_path, destination_path)
    
    print(f'Copied {file_name} to FINAL_COMBINED_PDF')