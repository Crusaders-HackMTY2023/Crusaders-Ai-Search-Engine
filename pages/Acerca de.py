import streamlit as st

# Datos ficticios de los miembros del equipo
equipo = [
    {
        "nombre": "Imanol González",
        "linkedin": "https://www.linkedin.com/in/imanolgzz/",
    },
    {
        "nombre": "Alfonso Molina",
        "linkedin": "https://www.linkedin.com/in/alfonso-enrique-molina-saucedo-a81370258/",
    },
    {
        "nombre": "Pedro Sánchez",
        "linkedin": "https://www.linkedin.com/in/carlosrodriguez/",
    },
    {
        "nombre": "Emilio Domínguez",
        "linkedin": "https://www.linkedin.com/in/marialopez/",
    }
]

# Descripción del proyecto
descripcion_proyecto = """
Este proyecto es una aplicación web que permite cargar un archivo PDF y realizar preguntas sobre su contenido. Utiliza tecnologías de procesamiento de lenguaje natural para analizar el texto del PDF y responder preguntas formuladas por el usuario. Nuestra misión es hacer que la extracción de información a partir de documentos PDF sea más rápida y accesible.

¡Esperamos que disfrutes usando nuestra aplicación!
"""

# Diseño de la página "About"
st.title("Acerca de Nosotros")
st.write(descripcion_proyecto)

st.title("Crusaders HackMTY 2023")
for miembro in equipo:
    st.subheader(miembro["nombre"])
    st.write(f"LinkedIn: [{miembro['nombre']}]({miembro['linkedin']})")
    #st.write(miembro["descripcion"])
    st.write("----")

# Puedes personalizar el diseño utilizando los elementos de estilo de Streamlit
# Por ejemplo, puedes usar st.image para mostrar fotos de los miembros del equipo.
