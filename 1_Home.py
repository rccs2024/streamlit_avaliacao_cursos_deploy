from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
from collections import Counter
import re
import nltk
nltk.download('stopwords')
from wordcloud import WordCloud
from nltk.corpus import stopwords

import matplotlib.pyplot as plt

# Definindo o layout da página Home
st.set_page_config(page_title="Dashboard Interativo", layout="wide")
st.markdown("""
    <style>
    /* Estilo da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #8d0333;  /* Usando a cor primária da UFMA */
    }

    /* Estilo do texto dos itens do menu usando a classe inspecionada */
    [data-testid="stSidebar"] .eczjsme5 {
        font-size: 18px;
        font-weight: bold;
        color: #FFFFFF !important; /* Define a cor do texto para branco */
    }

    /* Estilo padrão para os elementos de input como selectbox e button */
    [data-testid="stSidebar"] .stSelectbox, 
    [data-testid="stSidebar"] button {
        color: black !important;
    }
    /* Mudando a cor do texto que fica em cima do selectbox */
    [data-testid="stSidebar"] p {
        color: white; /* Altere para a cor que preferir */
        font-weight: bold; /* Fazendo o texto ficar em negrito */
    </style>
    """, unsafe_allow_html=True)

###### importando o dataframa Alunos e tratando as colunas #############
#exportando tabelas e tratanto 




# Adicionando o título principal
st.title("Dashboard de Avaliação de Cursos")

# Adicionando o texto introdutório
st.markdown("""
    Bem-vindo ao **Dashboard de Avaliação de Cursos** da Divisão de Capacitação e Desenvolvimento da UFMA. 
    Este painel interativo foi desenvolvido para fornecer uma visão abrangente das avaliações realizadas pelos participantes dos cursos ao longo dos anos.

    Aqui você encontrará:
    - **Análises detalhadas** sobre o desempenho dos instrutores e turmas em diferentes cursos.
    - **Médias de avaliação** por categorias e turmas para identificar áreas de destaque e pontos de melhoria.
    - **Visualização de dados** com gráficos interativos para uma compreensão mais fácil e dinâmica das informações.
    - **Comentários dos participantes** para um feedback mais qualitativo sobre as experiências nos cursos.

    Use o menu de navegação à esquerda para explorar as diferentes páginas e obter insights valiosos sobre o desempenho dos cursos e instrutores.

    **Nota:** Este dashboard é atualizado regularmente para garantir que você tenha sempre as informações mais recentes.
""")

# Se você tiver algum gráfico ou imagem que deseja exibir na página inicial, pode adicioná-lo aqui
# Exemplo de imagem na página inicial:
# st.image("img/ufma.png", caption="UFMA - Divisão de Capacitação e Desenvolvimento", use_column_width=True)

# Rodapé
st.markdown("<div style='position: fixed; bottom: 0; width: 100%; text-align: center; color: grey;'>Desenvolvido pela equipe da Divisão de Capacitação e Desenvolvimento da UFMA</div>", unsafe_allow_html=True)
st.markdown("<div style='position: fixed; bottom: 0; right: 0; color: grey;'>Última atualização: 20/09/2024</div>", unsafe_allow_html=True)
