"""
# Load txt file with document loader

from langchain_community.document_loaders import TextLoader

print('laod txt file with TextLoader..')

loader = TextLoader("test-document/notes.txt")

result1 = loader.load()
print(result1)
'''
[Document(metadata={'source': 'test-document/notes.txt'}, page_content='Hello Python\nLearning AI\n\n\n19-10\n12.30 se start  1:30\n2:10 start ')]
'''

print(result1[0].page_content)
print(result1[0].metadata) # {'source': 'test-document/notes.txt'}

#--------------------------------------------

# Load pdf file with PyPDF Loader

from langchain_community.document_loaders  import PyPDFLoader

print('PyPDFLoader..')

loader = PyPDFLoader("test-document/test-pdf.pdf")

result1 = loader.load()
print(result1[0].page_content)

print(result1[0].metadata)
'''
{'producer': 'Microsoft® Word for Microsoft 365', 'creator': 'Microsoft® Word for Microsoft 365', 'creationdate': '2026-10-19T14:15:44+05:30', 'author': 'Mohit Saxena', 'moddate': '2026-10-19T14:15:44+05:30', 'source': 'test-document/test-pdf.pdf', 'total_pages': 4, 'page': 0, 'page_label': '1'}
'''



#-------------------------------------------------

# Load multiple txt file from Directory with Directory Loader

print('Load multiple txt file from Directory with Directory Loader...')

from langchain_community.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader(
    "test-document/", 
    glob="*.txt", 
    loader_cls=TextLoader)

docs = loader.load()

print("Total documents:", len(docs))
print(docs[0].page_content)
print(docs[0].metadata)



# Load multiple pdf file from Directory with Directory Loader

print('Load multiple txt file from Directory with Directory Loader...')

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path= "test-document/", 
    glob="*.pdf", 
    loader_cls=PyPDFLoader)

docs = loader.load()

print("Total documents:", len(docs)) # 5

# the resulting document count generally corresponds to the total number of PDF pages, not the number of PDF files.

print(docs[5].page_content) #IndexError: list index out of range
print(docs[5].metadata) #IndexError: list index out of range

#-----------------------------



print('lazy_laod()...')

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path= "test-document/", 
    glob="*.pdf", 
    loader_cls=PyPDFLoader)

docs = loader.lazy_load()

print(docs) # <generator object DirectoryLoader.lazy_load at 0x0000023FB3584D30>

# use for loop on this docs object & it will print once doc loaded
for doc in docs:
    print(doc.metadata)
    


#----------------------------------------------------

# web based loader

print('Web based loader.....')

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader('https://www.samsung.com/in/smartphones/galaxy-m/galaxy-m17e-5g-blitz-blue-128gb-sm-m076blbbins/buy/?cid=in_pd_pmax_google_galaxy-m17_ongoing_m17-26-pmax-pla-lti-pfm_pla_product-kv_1ur-590041l-2026&utm_source=google&utm_medium=paid&utm_campaign=-23678709337--&utm_term=&gad_source=1&gad_campaignid=23678725111&gbraid=0AAAAADm5iQUPnjurkKf9HIX1pa43AzyUa&gclid=CjwKCAjw_9bWBhBGEiwAomyTImlNLfEsEMK4Nqt4l_gMIdrziwLYRsY-dfN9qZJAPOamdLqB6DJSrRoCK0AQAvD_BwE')

doc = loader.load()

print(doc[0].page_content)

print(doc[0].metadata)

"""

#--------------------------------------------

# CSV Loader

print('CSV Loader..')

from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("test-document/test-csv.csv", metadata_columns=['id'])

file = loader.load()

print("Total documents:", len(file))

print(file[0].page_content)
# id: 101
# name: Mouse
# description: Wireless mouse
# price: 799

print(file[0].metadata)


for row in file:
    line = row.page_content.splitlines()
    print(line)
    # ['id: 101', 'name: Mouse', 'description: Wireless mouse', 'price: 799']
   
# print only name field of each row
 
for row in file:
    line = row.page_content.splitlines()
    for item in line:
        if item.startswith('name:'):
            print(item)
# name: Mouse
# name: Keyboard
# name: Monitor
