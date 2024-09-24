from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
from collections import Counter
import re
from wordcloud import WordCloud
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt

# Definindo o layout da página Home
st.set_page_config(page_title="Dashboard Interativo", layout="wide")

###### importando o dataframa Alunos e tratando as colunas #############
#exportando tabelas e tratanto 

df_geral = pd.read_excel('../bd/df_analise.xlsx', decimal='.')
df_comentarios = pd.read_excel('../bd/df_comentarios.xlsx', decimal='.')

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
