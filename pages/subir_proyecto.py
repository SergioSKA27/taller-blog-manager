import streamlit as st
from st_xatadb_connection  import XataConnection,XataClient
from st_tiny_editor import tiny_editor
import asyncio
import requests


client = XataClient(st.secrets['XATA_API_KEY'],db_url=st.secrets['XATA_DB_URL'])
st.set_page_config(layout='wide')
xata = st.connection('xata',type=XataConnection)

#--------------------------------------------------------------------------
#Funciones
async def get_random_image(query='random'):
    try:
        result = await asyncio.to_thread(requests.get, f'https://source.unsplash.com/random/600x400?{query}',timeout=1)
        return result.content
    except Exception as e:
        print(e)
        return f"https://source.unsplash.com/random/600x400?{query}"


def get_projects():
    try:
        response = xata.query("Proyecto")
        return response
    except Exception as e:
        st.error(f'Error: {e}')
        return None


def update_projects():
    st.session_state.projects = get_projects()['records']


async def insert_project(title,url,contenido,embed):
    await asyncio.sleep(0.1)
    payload =  {
    "titulo": title,
    "url": url,
    "descripcion": contenido,
    "embed": embed
    }
    try:
        response = xata.insert("Proyecto", payload)
        st.write(response)
        st.toast('Proyecto añadido correctamente',icon='🎉')
    except Exception as e:
        st.error(f'Error: {e}')



if 'projects' not in st.session_state:
    st.session_state.projects = get_projects()['records']

st.title('Añadir Proyecto',help='Añade un nuevo proyecto a tu portafolio')
st.divider()
titulo = st.text_input('Titulo',help='Titulo del proyecto')
url = st.text_input('URL',help='URL del proyecto')

embed = st.toggle('Embed',False,help='Renderiza el proyecto en un iframe')

contenido = None
with st.form(key='editor_form'):
    contenido = tiny_editor(st.secrets['TINY_API_KEY'],
                            height=600,
                            key='welcomeeditor',
                            toolbar = 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | emoticons charmap | removeformat',
                            plugins = [
                              "advlist", "anchor", "autolink", "charmap", "code",
                              "help", "image", "insertdatetime", "link", "lists", "media",
                              "preview", "searchreplace", "table", "visualblocks", "accordion",'emoticons',
                              ]
                            )
    if st.form_submit_button('Vista previa',use_container_width=True):
        st.write(contenido,unsafe_allow_html=True)
        with st.expander('Ver HTML'):
            st.text(contenido)

if st.button('Añadir Proyecto',use_container_width=True):
    if titulo != '' and contenido is not None and url != '':
        asyncio.run(insert_project(titulo,url,contenido,embed))
        update_projects()
    else:
        st.error('Por favor rellena todos los campos')

