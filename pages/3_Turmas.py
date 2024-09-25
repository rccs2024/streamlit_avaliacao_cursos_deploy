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
            
    [data-testid="stSidebar"] .ef3psqc11 {
        background-color: #FEC84D;
      
    </style>

    
    """, unsafe_allow_html=True)




###### importando o dataframa Alunos e tratando as colunas #############
#exportando tabelas e tratanto 

df_geral = pd.read_excel('df_analise.xlsx', decimal='.')
df_comentarios = pd.read_excel('df_comentarios.xlsx', decimal='.')

# Função para limpar o texto e remover stopwords
def limpar_texto(texto):
    texto = re.sub(r'\W', ' ', str(texto))  # Remove pontuações
    texto = texto.lower()  # Converte para minúsculas
    texto = texto.split()  # Divide em palavras
    stop_words = set(stopwords.words('portuguese'))
    texto = [palavra for palavra in texto if palavra not in stop_words]  # Remove stopwords
    return ' '.join(texto)



st.markdown('# Turma')
st.divider()





# Filtro por ano
anos = df_geral['Ano Turma'].unique()
ano_selecionado = st.sidebar.selectbox('Selecione o Ano', sorted(anos))

# Filtro por curso
cursos = df_geral[df_geral['Ano Turma'] == ano_selecionado]['Turma'].unique()
curso_selecionado = st.sidebar.selectbox('Selecione o Curso', sorted(cursos))

# Adicionando um botão para atualizar as informações
atualizar = st.sidebar.button("Atualizar")

# Só realiza a atualização se o botão for clicado
if atualizar:
    #df_geral = df_geral.reset_index()
    # Filtrar o dataframe pelo ano e curso selecionados
    df_curso_selecionado = df_geral[(df_geral['Ano Turma'] == ano_selecionado) & (df_geral['Turma'] == curso_selecionado)]
    df_comentarios_selecionado = df_comentarios[df_comentarios['Turma'] == curso_selecionado]
    
   
    # Exibir média das avaliações por categoria
    st.markdown(f"## {curso_selecionado.title()}")
    col1, col2 = st.columns(2)
    col1.markdown(f"### Ano: {ano_selecionado}")
   # Pegando os instrutores únicos e unindo em uma string
    instrutores = ', '.join(df_comentarios_selecionado['Instrutor'].unique())
    col2.markdown(f"#### Instrutor(es): {instrutores.title()}")
    st.divider()

    # Calcular os totais gerais
    comparativo_aprovados =  df_curso_selecionado.groupby('Turma').agg({'Total_Avaliacao': 'first', 'Aprovados': 'first'}).reset_index()# Calcular a porcentagem de aprovados
    avaliacao = comparativo_aprovados['Total_Avaliacao']
    aprovado = comparativo_aprovados['Aprovados']
    media_avaliacao = (comparativo_aprovados['Total_Avaliacao'].sum() / comparativo_aprovados['Aprovados'].sum()) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total de Aprovados", value=int(aprovado))
    col2.metric(label="Total de Avaliações", value=int(avaliacao))
    col3.metric(label="Pecentual de Avaliações realizadas (%)", value=f"{media_avaliacao:.2f}%")
    # Criando um gráfico de barras para mostrar a avaliação por categoria
    fig = px.bar(df_curso_selecionado, 
                 x='Categoria', 
                 y=['Ótimo (%)', 'Bom (%)', 'Regular (%)', 'Fraco (%)'], 
                 title=f"Avaliações por Categoria - {curso_selecionado} ({ano_selecionado})",
                 labels={'value': 'Porcentagem', 'Categoria': 'Categoria'},
                 barmode='group')

    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)

    # Exibir a tabela de avaliações na primeira coluna
    with col1:
        st.markdown("### Detalhes por Categoria")
        st.dataframe(df_curso_selecionado[['Categoria', 'Questão', 'Ótimo (%)', 'Bom (%)', 'Regular (%)', 'Fraco (%)']].set_index('Categoria'), height=600)

    # Exibir os comentários na segunda coluna
    with col2:
        st.markdown("### Comentários dos Participantes")
        if not df_comentarios_selecionado.empty:
            st.dataframe(df_comentarios_selecionado[['Comentário']].reset_index(drop=True), height=600)
        else:
            st.write("Nenhum comentário disponível para este curso.")
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # Nuvem de palavras
        st.markdown("### Nuvem de Palavras dos Comentários")
        df_comentarios_selecionado['Comentario_limpo'] = df_comentarios_selecionado['Comentário'].apply(limpar_texto)
        todos_comentarios = ' '.join(df_comentarios_selecionado['Comentario_limpo'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(todos_comentarios)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

    with col2:
        # Classificação dos comentários
        st.markdown("### Classificação dos Comentários")
        palavras_positivas = ["excelente", "ótimo", "bom", "parabéns", "maravilhoso", "incrível", "satisfatório","boa","agregaram","excelentes"]
        palavras_negativas = ["ruim", "péssimo", "não gostei", "horrível", "insatisfatório", "fraco", "problema"]
        palavras_neutras = ["ok", "regular", "aceitável", "mediano", "neutro"]

        def classificar_comentario(comentario):
            comentario = comentario.lower()
            if any(palavra in comentario for palavra in palavras_positivas):
                return "Positivo"
            elif any(palavra in comentario for palavra in palavras_negativas):
                return "Negativo"
            elif any(palavra in comentario for palavra in palavras_neutras):
                return "Neutro"
            else:
                return "Neutro"

        # Aplicar a função de classificação
        df_comentarios_selecionado['Classificacao_Regras'] = df_comentarios_selecionado['Comentário'].apply(classificar_comentario)

        # Verificar se o DataFrame não está vazio
        if len(df_comentarios_selecionado) > 0:
            # Contar as classificações dos comentários e garantir que o DataFrame tenha as colunas corretas
            classificacao_counts = df_comentarios_selecionado['Classificacao_Regras'].value_counts().reset_index()
            classificacao_counts.columns = ['Classificacao', 'Contagem']  # Renomeando as colunas para facilitar o uso

            # Criar o gráfico com plotly express
            fig = px.bar(classificacao_counts,
                        x='Classificacao', 
                        y='Contagem', 
                        labels={'Classificacao': 'Classificação', 'Contagem': 'Número de Comentários'},
                        #title='Distribuição de Classificações dos Comentários (Regras)',
                        color='Classificacao', 
                        color_discrete_map={'Neutro': '#FEC84D', 'Positivo': '#0AB0AB', 'Negativo': '#FF5733'})

            fig.update_layout(
                xaxis_title="Classificação",
                yaxis_title="Número de Comentários",
                showlegend=False
            )

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig, use_container_width=True)
else:
    df_geral = df_geral.reset_index()
    media_avaliacoes_curso = df_geral.groupby('Turma')[['Ótimo (%)', 'Bom (%)', 'Regular (%)', 'Fraco (%)']].mean()
    
    # Calcular a média geral das avaliações por categoria de todos os cursos
    media_categoria = df_geral.groupby('Categoria')[['Ótimo (%)', 'Bom (%)', 'Regular (%)', 'Fraco (%)']].mean().reset_index()

    # Transformar o DataFrame para o formato longo
    media_categoria_long = media_categoria.melt(id_vars='Categoria', 
                                                value_vars=['Ótimo (%)', 'Bom (%)', 'Regular (%)', 'Fraco (%)'],
                                                var_name='Tipo de Avaliação', 
                                                value_name='Média (%)')
    
    # Criar o gráfico de barras para exibir as médias gerais por categoria (ajustado para orientação vertical)
    fig_media_categoria = px.bar(media_categoria_long, 
                                 y='Categoria', 
                                 x='Média (%)', 
                                 color='Tipo de Avaliação', 
                                 orientation='h',
                                 barmode='group',
                                 title='Média das Avaliações por Categoria de Todos os Cursos',
                                 labels={'Média (%)': 'Média (%)', 'Categoria': 'Categoria'},
                                 color_discrete_map={'Ótimo (%)': '#8D0333', 'Bom (%)': '#FEC84D', 'Regular (%)': '#0AB0AB', 'Fraco (%)': 'red'})

    col1, col2 = st.columns([1, 1])  # Dividindo o espaço em duas colunas

    with col1:
        st.dataframe(media_avaliacoes_curso, height=800)
    
    with col2:
        st.plotly_chart(fig_media_categoria, use_container_width=True)

# Rodapé
#st.markdown("<p style='text-align: center; color: grey;'>Desenvolvido pela equipe da Divisão de Capacitação e Desenvolvimento da UFMA</p>", unsafe_allow_html=True)
#st.markdown("<p style='text-align: right; color: grey;'>Última atualização: 20/09/2024</p>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.image("img/ufma.png", use_column_width=True)

st.markdown("<div style='position: fixed; bottom: 0; width: 100%; text-align: center; color: grey;'>Desenvolvido pela equipe da Divisão de Capacitação e Desenvolvimento da UFMA</div>", unsafe_allow_html=True)
st.markdown("<div style='position: fixed; bottom: 0; right: 0; color: grey;'>Última atualização: 20/09/2024</div>", unsafe_allow_html=True)