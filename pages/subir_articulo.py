import streamlit as st
from st_xatadb_connection  import XataConnection
from st_tiny_editor import tiny_editor
import asyncio


st.set_page_config(layout='wide')
xata = st.connection('xata',type=XataConnection)
if 'login' not in st.session_state or not st.session_state.login:
    st.switch_page(page='Login.py')


async def insert_article(title,tags,banner,contenido):
    await asyncio.sleep(0.1)
    payload = {
    "titulo": title,
    "contenido": contenido,
    "tags": tags,
    }
    try:
        response = xata.insert("Articulo", payload)
        st.write(response)
        st.success('Articulo añadido correctamente',icon='🎉')
    except Exception as e:
        st.error(f'Error: {e}')

    try:
        if banner is not None:
            fresponse = xata.upload_file('Articulo',response['id'],'banner',banner.getvalue(),banner.type)
            st.write(fresponse)
            st.success('Banner añadido correctamente',icon='🎉')
    except Exception as e:
        st.error(f'Error al subir el banner: {e}')


def get_articles():
    try:
        response = xata.query("Articulo")
        return response
    except Exception as e:
        st.error(f'Error: {e}')
        return None


def update_articles():
    st.session_state.articles = get_articles()['records']

if 'articles' not in st.session_state:
    st.session_state.articles = get_articles()['records']


st.title('Añadir Articulo')



titulo = st.text_input('Titulo')
tags = ['python','streamlit','xata','data','data-science','programming','machine-learning','deep-learning','artificial-intelligence','data-visualization','data-analysis','data-engineering']

tg = st.multiselect('Tags',tags,placeholder='Selecciona los tags',max_selections=5,help='Selecciona los tags que mejor describan tu articulo')

banner = st.file_uploader('Banner',type=['png','jpg','jpeg'],)



if banner:
    st.image(banner.read(),width=300)

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


    if st.form_submit_button('Vista previa',use_container_width=True) and contenido:
        st.markdown(contenido,unsafe_allow_html=True)
        with st.expander('Ver HTML'):
            st.text(contenido)

if titulo != '' and contenido and len(tg) > 0:
    if st.button('Publicar',use_container_width=True):
        asyncio.run(insert_article(titulo,tg,banner,contenido))
        update_articles()

