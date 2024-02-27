import streamlit as st
from st_xatadb_connection  import XataConnection,XataClient
from st_tiny_editor import tiny_editor
import asyncio
import time
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


def get_articles():
    try:
        response = xata.query("Articulo")
        return response
    except Exception as e:
        st.error(f'Error: {e}')
        return None


def update_articles():
    st.session_state.articles = get_articles()['records']

def set_editor(article):
    st.session_state.article = article

def delete_article(article_id):
    try:
        response = xata.delete("Articulo",article_id)
        st.write(response)
        st.toast('Articulo eliminado correctamente',icon='🎉')
        time.sleep(1)
        update_articles()
    except Exception as e:
        st.error(f'Error: {e}')

def render_article(article):
    with st.container(border=True):
        if 'banner' in article and 'url' in article['banner']:
            st.image(article['banner']['url'],use_column_width=True)
        else:
            with st.spinner('Cargando imagen'):
                im = asyncio.run(get_random_image(','.join(article['tags'])))
                st.image(im,use_column_width=True)


        st.write(f'## {article["titulo"]}')
        st.write(f'### Tags: {", ".join(article["tags"])}')
        bc1,bc2 = st.columns(2,gap='small')
        bc1.button('Editar',key=f'edit_{article["id"]}',use_container_width=True,on_click=set_editor,args=(article,))
        bc2.button(':red[Eliminar]',on_click=delete_article,args=(article['id'],),key=f'delete_{article["id"]}',use_container_width=True)

def render_editor():
    cc,cb = st.columns([0.9,0.1])
    cc.header('Editar Articulo')
    if cb.button('Cerrar',key='close_editor',use_container_width=True):
        st.session_state.article = None
        st.rerun()

    titulo = st.text_input('Titulo',value=st.session_state.article['titulo'])
    tags = ['python','streamlit','xata','data','data-science','programming','machine-learning','deep-learning','artificial-intelligence','data-visualization','data-analysis','data-engineering']
    tg = st.multiselect('Tags',tags,default=st.session_state.article['tags'],max_selections=5,help='Selecciona los tags que mejor describan tu articulo')
    banner = st.file_uploader('Banner',type=['png','jpg','jpeg'],)
    if banner:
        st.image(banner.read(),width=300)

    contenido = None
    with st.form(key='editor_form1'):
        contenido = tiny_editor(st.secrets['TINY_API_KEY'],
                                initialValue=st.session_state.article['contenido'],
                                height=600,
                                key='welcomeeditor1',
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
    if st.button('Guardar cambios'):
        payload = {}
        if titulo != st.session_state.article['titulo']:
            payload['titulo'] = titulo
        if tg != st.session_state.article['tags']:
            payload['tags'] = tg
        if contenido != st.session_state.article['contenido']:
            payload['contenido'] = contenido
        if len(payload)>0:
            try:
                response = xata.update("Articulo",st.session_state.article['id'],payload)
                st.write(response)
                st.success('Articulo actualizado correctamente',icon='🎉')
                time.sleep(1)
                update_articles()
                st.session_state.article = None
                st.rerun()
            except Exception as e:
                st.error(f'Error: {e}')

if 'articles' not in st.session_state:
    st.session_state.articles = get_articles()['records']

if 'article' not in st.session_state:
    st.session_state.article = None

cols = st.columns(3)
k= 0






if st.session_state.article:
    render_editor()

else:
    for article in st.session_state.articles:
        with cols[k]:
            render_article(article)
        k+=1
        if k==3:
            k=0
