import io
import sys
import os
import PyPDF2
from softtek_llm.chatbot import Chatbot
from softtek_llm.models import OpenAI
from softtek_llm.cache import Cache
from softtek_llm.vectorStores import PineconeVectorStore
from softtek_llm.embeddings import OpenAIEmbeddings
from softtek_llm.schemas import Filter
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader

def initialize_chatbot():
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
    if OPENAI_API_BASE is None:
        raise ValueError("OPENAI_API_BASE not found in .env file")

    OPENAI_EMBEDDINGS_MODEL_NAME = os.getenv("OPENAI_EMBEDDINGS_MODEL_NAME")
    if OPENAI_EMBEDDINGS_MODEL_NAME is None:
        raise ValueError("OPENAI_EMBEDDINGS_MODEL_NAME not found in .env file")

    OPENAI_CHAT_MODEL_NAME = os.getenv("OPENAI_CHAT_MODEL_NAME")
    if OPENAI_CHAT_MODEL_NAME is None:
        raise ValueError("OPENAI_CHAT_MODEL_NAME not found in .env file")
    
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    if PINECONE_API_KEY is None:
        raise ValueError("PINECONE_API_KEY not found in .env file")

    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    if PINECONE_ENVIRONMENT is None:
        raise ValueError("PINECONE_ENVIRONMENT not found in .env file")

    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    if PINECONE_INDEX_NAME is None:
        raise ValueError("PINECONE_INDEX_NAME not found in .env file")

    vector_store = PineconeVectorStore(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT,
        index_name=PINECONE_INDEX_NAME,
    )
    embeddings_model = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model_name=OPENAI_EMBEDDINGS_MODEL_NAME,
        api_type="azure",
        api_base=OPENAI_API_BASE,
    )
    cache = Cache(
        vector_store=vector_store,
        embeddings_model=embeddings_model 
    ) 
    model = OpenAI(
        api_key=OPENAI_API_KEY,
        model_name=OPENAI_CHAT_MODEL_NAME,
        api_type="azure",
        api_base=OPENAI_API_BASE,
        verbose=True,
    )

    filters = [
        Filter(
            type="DENY",
            case="",

        ),
    ]

    chatbot = Chatbot(
        model=model,
        #cache=cache,
        #filters=filters,
        #description="You are a polite and very helpful assistant",
    )
    
    return chatbot
"""
def get_chatbot_response(question, chatbot):
    response = chatbot.chat(
        question,
        cache_kwargs={"namespace": "chatbot-cache-test"},
        print_cache_score=False,
    )
    
    return response.message.content
"""


"""
def get_chatbot_response(question, chatbot, max_attempts=5):
    attempts = 0
    
    while attempts < max_attempts:
        try:
            response = chatbot.chat(
                question,
                cache_kwargs={"namespace": "chatbot-cache-test"},
                print_cache_score=False,
            )
            return response.message.content
        except Exception as e:
            attempts += 1
            print(f"Error (intentos restantes: {max_attempts - attempts}): {str(e)}")
    
    return "Se agotaron los intentos. No se pudo obtener una respuesta del chatbot."
"""
    

def get_chatbot_response(question, chatbot):
    try:
        # Redirigir la salida estándar a response_buffer
        response_buffer = io.StringIO()
        sys.stdout = response_buffer
        response = chatbot.chat(
            question,
            cache_kwargs={"namespace": "chatbot-cache-test"},
            print_cache_score=True,
            
        )
        sys.stdout = sys.__stdout__

        return response.message.content
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Ocurrió un error al obtener la respuesta del chatbot."

def readPDF(fileName):
    loader = PyPDFLoader(fileName)
    pages = loader.load_and_split()

    stringTemp=""

    for i in range(len(pages)):
        #print(pages[i].__str__())
        stringTemp+=pages[i].__str__()
    
    return stringTemp


def main():
    chatbot = initialize_chatbot()
    print("Bienvenido al Chatbot de crusaders, escriba su pregunta o teclee q para salir en cualquier momento")
    print(" ")
    # auxiliar = readPDF("ResearchCovid.pdf")
    # response = get_chatbot_response("Resume el siguiente texto: " + auxiliar, chatbot)
    # print(response)
    
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            break
        
        response = get_chatbot_response(user_input, chatbot)
        print(response)
        print(" ")

if __name__ == "__main__":
    main()