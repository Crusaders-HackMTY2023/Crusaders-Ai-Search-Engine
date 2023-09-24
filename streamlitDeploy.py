import streamlit as st
import io
import sys
import os
import tempfile
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

# Función para leer el contenido de un PDF desde un archivo cargado por el usuario
def readPDF(uploaded_file):
    if uploaded_file is not None:
        # Crear un archivo temporal para almacenar el contenido del PDF
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            pdf_path = temp_file.name

        # Inicializar el cargador de PDF con la ruta del archivo
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()

        # Concatenar el contenido de las páginas en una cadena
        pdf_content = ""
        for page in pages:
            pdf_content += page.__str__()

        # Eliminar el archivo temporal
        os.remove(pdf_path)

        return pdf_content
    else:
        return ""
# Crear la interfaz de usuario con Streamlit
def main():
    st.title("CRUSADERS ENGINE")
    st.write("Bienvenido al Chatbot de Crusaders")

    # Agregar un campo de carga de archivo PDF
    uploaded_file = st.file_uploader("Cargar archivo PDF", type=["pdf"])

    if uploaded_file is not None:
        # Mostrar el nombre del archivo cargado
        st.write(f"Archivo cargado: {uploaded_file.name}")

        # Leer el contenido del archivo PDF
        pdf_text = readPDF(uploaded_file)
        #st.write("Texto extraído del PDF:")
        #st.text(pdf_text)

        # Inicializar el chatbot
        chatbot = initialize_chatbot()

        # Agregar un campo de entrada de texto para preguntas
        user_input = st.text_input("Ingrese su pregunta, dejar en blanco si desea un resumen:")

        if st.button("Submit"):
            if user_input:
                # Obtener la respuesta del chatbot y mostrarla
                response = get_chatbot_response(user_input + pdf_text, chatbot)
                st.write("Respuesta del Chatbot:")
                st.markdown(response)
            else:
                # Obtener el resumen del PDF y mostrarlo
                response = get_chatbot_response("Resume el siguiente texto: " + pdf_text, chatbot)
                st.write("Resumen del PDF:")
                st.markdown(response)

if __name__ == "__main__":
    main()