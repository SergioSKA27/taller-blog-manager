import streamlit as st
from st_xatadb_connection  import XataConnection
import bcrypt

st.set_page_config(layout='centered')
xata = st.connection('xata',type=XataConnection)

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .bg {
        background-image:  url("data:image/svg+xml;utf8,%3Csvg width=%222000%22 height=%221000%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cdefs%3E%3ClinearGradient id=%22a%22 gradientTransform=%22rotate(90)%22%3E%3Cstop offset=%225%25%22 stop-color=%22%2365a6da%22%2F%3E%3Cstop offset=%2295%25%22 stop-color=%22%238bbce3%22%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient id=%22b%22 gradientTransform=%22rotate(90)%22%3E%3Cstop offset=%225%25%22 stop-color=%22%2392b8d8%22%2F%3E%3Cstop offset=%2295%25%22 stop-color=%22%23adc9e1%22%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient id=%22c%22 gradientTransform=%22rotate(90)%22%3E%3Cstop offset=%225%25%22 stop-color=%22%23becbd5%22%2F%3E%3Cstop offset=%2295%25%22 stop-color=%22%23ced8df%22%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient id=%22d%22 gradientTransform=%22rotate(90)%22%3E%3Cstop offset=%225%25%22 stop-color=%22%23d7d7d7%22%2F%3E%3Cstop offset=%2295%25%22 stop-color=%22%23e1e1e1%22%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient id=%22e%22 gradientTransform=%22rotate(90)%22%3E%3Cstop offset=%225%25%22 stop-color=%22%23ddd%22%2F%3E%3Cstop offset=%2295%25%22 stop-color=%22%23e5e5e5%22%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient id=%22f%22 gradientTransform=%22rotate(90)%22%3E%3Cstop offset=%225%25%22 stop-color=%22%23e4e4e4%22%2F%3E%3Cstop offset=%2295%25%22 stop-color=%22%23eaeaea%22%2F%3E%3C%2FlinearGradient%3E%3ClinearGradient id=%22g%22 gradientTransform=%22rotate(90)%22%3E%3Cstop offset=%225%25%22 stop-color=%22%23eaeaea%22%2F%3E%3Cstop offset=%2295%25%22 stop-color=%22%23efefef%22%2F%3E%3C%2FlinearGradient%3E%3C%2Fdefs%3E%3Cpath fill=%22%233993dd%22 d=%22M0 0h2000v1000H0z%22%2F%3E%3Cpath d=%22M0 125c61.42-16.948 122.838-33.896 170-30 47.162 3.896 80.066 28.638 124 44 43.934 15.362 98.898 21.346 154 20 55.102-1.346 110.341-10.02 158-26 47.659-15.98 87.737-39.266 141-42 53.263-2.734 119.71 15.082 183 25 63.29 9.918 123.422 11.936 166 6s67.6-19.826 121-10c53.4 9.826 135.177 43.366 187 44 51.823.634 73.693-31.64 121-43s120.051-1.808 176 10 95.102 25.871 149 19c53.898-6.871 122.542-34.678 150-41 27.458-6.322 13.729 8.839 40 24l-40 875H0Z%22 fill=%22url(%23a)%22%2F%3E%3Cpath d=%22M0 250c61.245-8.686 122.49-17.372 168-20 45.51-2.628 75.286.8 119 7s101.367 15.169 161 27c59.633 11.831 121.248 26.523 179 22 57.752-4.523 111.643-28.263 154-44 42.357-15.737 73.18-23.473 123-7 49.82 16.473 118.635 57.155 172 52 53.365-5.155 91.28-56.148 143-72 51.72-15.852 117.243 3.436 176 22 58.757 18.564 110.747 36.402 158 30 47.253-6.402 89.769-37.046 139-47 49.231-9.954 105.178.782 163 13s117.52 25.92 142 29c24.48 3.08 13.74-4.46 43-12l-40 750H0Z%22 fill=%22url(%23b)%22%2F%3E%3Cpath d=%22M0 375c39.52 15.465 79.04 30.93 132 24 52.96-6.93 119.363-36.255 182-39 62.637-2.745 121.51 21.092 168 20 46.49-1.092 80.596-27.111 127-27 46.404.111 105.105 26.354 160 37 54.895 10.646 105.982 5.695 153 5 47.018-.695 89.965 2.866 139-9s104.157-39.16 162-34c57.843 5.16 118.407 42.77 177 55 58.593 12.23 115.214-.922 159-9s74.736-11.083 123-9c48.264 2.083 113.84 9.253 172 4s108.903-22.93 132-28c23.097-5.07 18.549 2.465 54 10l-40 625H0Z%22 fill=%22url(%23c)%22%2F%3E%3Cpath d=%22M0 500c43.635 10.484 87.27 20.967 141 15 53.73-5.967 117.552-28.386 168-40 50.448-11.614 87.52-12.423 143-7 55.48 5.423 129.365 17.079 185 24 55.635 6.921 93.018 9.109 137 10s94.564.487 145 10c50.436 9.513 100.727 28.943 153 21 52.273-7.943 106.526-43.258 155-55 48.474-11.742 91.167.088 140-2s103.806-18.095 164-6c60.194 12.095 125.609 52.294 174 53 48.391.706 79.76-38.08 137-44 57.24-5.92 140.355 21.023 171 30 30.645 8.977 8.823-.011 27-9l-40 500H0Z%22 fill=%22url(%23d)%22%2F%3E%3Cpath d=%22M0 625c40.732 16.48 81.463 32.959 134 34 52.537 1.041 116.879-13.356 173-14 56.121-.644 104.022 12.465 152 14 47.978 1.535 96.034-8.502 148-21 51.966-12.498 107.84-27.455 163-39 55.16-11.545 109.604-19.676 163-12 53.396 7.676 105.745 31.161 158 37 52.255 5.839 104.415-5.968 147-15 42.585-9.032 75.594-15.29 132-19 56.406-3.71 136.208-4.876 191 11 54.792 15.876 84.573 48.791 124 51 39.427 2.209 88.5-26.29 154-43s147.429-21.631 177-17c29.571 4.631 6.786 18.816 24 33l-40 375H0Z%22 fill=%22url(%23e)%22%2F%3E%3Cpath d=%22M0 750c49.957-17.962 99.915-35.925 152-36 52.085-.075 106.3 17.737 157 26 50.7 8.263 97.889 6.976 155-2 57.111-8.976 124.145-25.643 173-24 48.855 1.643 79.532 21.595 122 33 42.468 11.405 96.729 14.264 149 15 52.271.736 102.553-.65 161-7s125.06-17.663 179-26 95.21-13.699 136 1c40.79 14.699 81.101 49.458 134 47 52.899-2.458 118.385-42.133 171-46 52.615-3.867 92.358 28.074 155 42 62.642 13.926 148.183 9.836 178 3 29.817-6.836 3.908-16.418 18-26l-40 250H0Z%22 fill=%22url(%23f)%22%2F%3E%3Cpath d=%22M0 875c42.187-13.59 84.373-27.178 131-17 46.627 10.178 97.694 44.124 158 44 60.306-.124 129.85-34.318 182-47 52.15-12.682 86.906-3.852 130-2 43.094 1.852 94.526-3.275 149-4 54.474-.725 111.99 2.953 164 9 52.01 6.047 98.515 14.465 157 24s128.95 20.187 178 12c49.05-8.187 76.682-35.213 124-45 47.318-9.787 114.323-2.335 165 8 50.677 10.335 85.027 23.554 138 27 52.973 3.446 124.57-2.88 187-8 62.43-5.12 115.694-9.034 137-9 21.306.034 10.653 4.017 40 8l-40 125H0Z%22 fill=%22url(%23g)%22%2F%3E%3C%2Fsvg%3E");
        bottom:0;
        left:-50%;
        opacity:1;
        position:fixed;
        right:-50%;
        top:0;
        z-index:0;
        background-size: cover;
        background-position: center center;
        background-repeat: repeat;
        width: 149%;
        height: 100%;
    }
</style>
<div class="bg"></div>
""",unsafe_allow_html=True)


def register_user(username,password):
    try:
        response = xata.insert("Usuario",{"username":username,"password":bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')})
        st.write(response)
        st.toast('Usuario registrado correctamente',icon='🎉')
        st.balloons()
    except Exception as e:
        st.error(f'Error: {e}')

st.title('Registro')

with st.form(key='registro'):
    username = st.text_input('Usuario')
    pass1 = st.text_input('Contraseña',type='password')
    pass2 = st.text_input('Repetir Contraseña',type='password')

    if st.form_submit_button('Registrar',use_container_width=True):
        if pass1 == pass2:
            if username != '' and pass1 != '':
                register_user(username,pass1)
            else:
                st.error('El usuario y la contraseña no pueden estar vacios')
        else:
            st.error('Las contraseñas no coinciden')
