
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("LecturaPDF.pdf")
pages = loader.load_and_split()

stringTemp=""

for i in range(len(pages)):
    #print(pages[i].__str__())
    stringTemp+=pages[i].__str__()

print(stringTemp)
