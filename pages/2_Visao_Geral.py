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

#### funções
# Função para limpar o texto e remover stopwords
def limpar_texto(texto):
    texto = re.sub(r'\W', ' ', str(texto))  # Remove pontuações
    texto = texto.lower()  # Converte para minúsculas
    texto = texto.split()  # Divide em palavras
    stop_words = set(stopwords.words('portuguese'))
    texto = [palavra for palavra in texto if palavra not in stop_words]  # Remove stopwords
    return ' '.join(texto)

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


df_geral = pd.read_excel('df_analise.xlsx', decimal='.')
df_comentarios = pd.read_excel('df_comentarios.xlsx', decimal='.')

#st.sidebar.image("img/ufma.png", use_column_width=True)


#st.markdown("""
#    <style>
#    /* Mudando a cor da sidebar */
#    [data-testid="stSidebar"] {
#        background-color: #8c0333;
#    }
#    /* Mudando a cor de todos os textos da sidebar */
#    [data-testid="stSidebar"] * {
#        color: white;
#    }
#    
#    /* Reduzindo o tamanho da logo */
#    .css-1d391kg img {
#        width: 100px; /* Altere o tamanho conforme necessário */
#        height: auto; /* Mantém a proporção da imagem */
#        display: block;
#        margin-left: auto;
#        margin-right: auto;
#    
#    }
#    </style>
#    """, unsafe_allow_html=True)




#Consultas pandas necessaria para gerar os graficos
# Média das avaliações por curso
media_avaliacoes_curso = df_geral.groupby('Turma')[['Ótimo (%)', 'Bom (%)', 'Regular (%)', 'Fraco (%)']].mean()
media_geral = media_avaliacoes_curso[['Ótimo (%)', 'Bom (%)', 'Regular (%)', 'Fraco (%)']].mean()

comparativo_aprovados = df_geral.groupby('Turma').agg({'Total_Avaliacao': 'first', 'Aprovados': 'first'}).reset_index()# Calcular a porcentagem de aprovados

#comparativo_aprovados['Percentual_Avaliação'] = (comparativo_aprovados['Total_Avaliacao'] / comparativo_aprovados['Aprovados']) * 100

# Calcular os totais gerais
total_avaliacoes_geral = comparativo_aprovados['Total_Avaliacao'].sum()
total_aprovados_geral = comparativo_aprovados['Aprovados'].sum()


####### Bloco de codigo para grafico pizza sobre da media geral
# Converter a média geral em um DataFrame para usar com plotly
df_media_geral = pd.DataFrame({
    'Tipo de Avaliação': media_geral.index,
    'Média (%)': media_geral.values
})

############# Geração de Grafico para visualizar media geral das avaliações dos cursos #########################################
fig = px.pie(df_media_geral,
             names='Tipo de Avaliação',
             values='Média (%)',
             title='Média Geral das Avaliações dos Cursos',
             color='Tipo de Avaliação',  # Define a cor de cada fatia com base no tipo de avaliação
             color_discrete_map={'Ótimo (%)': '#8D0333', 'Bom (%)': '#FEC84D', 'Regular (%)': '#0AB0AB', 'Fraco (%)': 'red'})

# Adicionar os valores percentuais dentro das fatias do gráfico
fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.02, 0.02, 0.02, 0.02]) 
fig.update_layout(showlegend=False)
#####  fim do bloco codigo para grafico pizza sobre da media geral #################################################################


####### Bloco de codigo para Comparação entre Total de Avaliações e Total de Aprovados nos Cursos #####################################
# Criar um DataFrame para os dados
df_dados = pd.DataFrame({
    'Categoria': ['Avaliações', 'Aprovados'],
    'Quantidade': [total_avaliacoes_geral, total_aprovados_geral]
})

# Criar o gráfico de barras com Plotly Express
fig2 = px.bar(df_dados,
             x='Categoria',
             y='Quantidade',
             title='Comparação entre Total de Avaliações e Total de Aprovados nos Cursos',
             labels={'Quantidade': 'Quantidade', 'Categoria': 'Categoria'},
             color='Categoria',  # Define cores diferentes para cada categoria
             color_discrete_map={'Avaliações': '#8D0333', 'Aprovados': '#FEC84D'})

fig2.update_layout(
    xaxis_title=None,  # Remove o título do eixo x
    #yaxis_title=None,  # Remove o título do eixo y
    #xaxis=dict(showticklabels=False),  # Remove os rótulos das categorias no eixo x
    #yaxis=dict(showticklabels=False),   # Remove os rótulos de valores no eixo y
    showlegend=False
)
####### Fim Bloco de codigo para Comparação entre Total de Avaliações e Total de Aprovados nos Cursos ####################################


####### Bloco de codigo para Comparação entre Total de Avaliações e Total de Aprovados nos Cursos por ano ################################
# Agrupando o DataFrame pelo 'Turma' e obtendo o primeiro registro para 'Total_Avaliacao' e 'Aprovados'
df_ajustado = df_geral.groupby(['Ano Turma', 'Turma']).agg({'Total_Avaliacao': 'first', 'Aprovados': 'first'}).reset_index()

# Agora, somamos os valores agregados por ano
df_comparativo_ajustado = df_ajustado.groupby('Ano Turma').agg(
    total_avaliacoes=('Total_Avaliacao', 'sum'),
    total_aprovados=('Aprovados', 'sum')
).reset_index()

# Transformar os dados para o formato long necessário para Plotly
df_comparativo_ajustado = df_comparativo_ajustado.melt(id_vars='Ano Turma', 
                                                       value_vars=['total_avaliacoes', 'total_aprovados'],
                                                       var_name='Categoria', 
                                                       value_name='Quantidade')

# Renomeando os valores da coluna 'Categoria' para melhorar a legibilidade
df_comparativo_ajustado['Categoria'] = df_comparativo_ajustado['Categoria'].replace({
    'total_avaliacoes': 'Avaliações',
    'total_aprovados': 'Aprovados'
})

# Criando o gráfico de barras agrupadas com Plotly
fig3 = px.bar(df_comparativo_ajustado, 
             x='Ano Turma', 
             y='Quantidade', 
             color='Categoria', 
             barmode='group',
             text='Quantidade',  # Adicionando os rótulos nas barras
             labels={"Ano Turma": "Ano", "Quantidade": "Quantidade"},
             title="Comparação entre Total de Avaliações e Total de Aprovados por Ano",
             color_discrete_map={'Avaliações': '#8D0333', 'Aprovados': '#FEC84D'}  # Aplicando a paleta de cores personalizada
            )

# Ajustar o layout do gráfico
fig3.update_layout(showlegend=True)
fig3.update_traces(textposition='outside')  # Posicionando o texto acima das barras

####### fim do Bloco de codigo para Comparação entre Total de Avaliações e Total de Aprovados nos Cursos por ano ################################

############# Grafico para visualizar media geral das avaliações dos cursos por ano #########################################
 #Criando o DataFrame de comparação anual
df_long_format = df_geral.groupby(['Ano Turma']).agg(
    avg_otimo=('Ótimo (%)', 'mean'),
    avg_bom=('Bom (%)', 'mean'),
    avg_regular=('Regular (%)', 'mean'),
    avg_fraco=('Fraco (%)', 'mean')
).reset_index()

# Transformando o DataFrame para formato long (necessário para plotagens mais eficazes)
df_long_format = df_long_format.melt(id_vars='Ano Turma', 
                                     value_vars=['avg_otimo', 'avg_bom', 'avg_regular', 'avg_fraco'],
                                     var_name='Avaliação', 
                                     value_name='Média (%)')

# Renomeando as colunas para melhor legibilidade
df_long_format['Avaliação'] = df_long_format['Avaliação'].replace({
    'avg_otimo': 'Ótimo (%)',
    'avg_bom': 'Bom (%)',
    'avg_regular': 'Regular (%)',
    'avg_fraco': 'Fraco (%)'
})

# Definindo o mapeamento de cores conforme o ajuste solicitado
custom_colors = {
    'Ótimo (%)': '#8D0333',   # Cor especificada para Ótimo
    'Bom (%)': '#FEC84D',     # Cor especificada para Bom
    'Regular (%)': '#0AB0AB', # Cor especificada para Regular
    'Fraco (%)': 'red'        # Cor especificada para Fraco
}

# Criando o gráfico com Plotly
fig4 = px.bar(df_long_format, 
             x='Ano Turma', 
             y='Média (%)', 
             color='Avaliação', 
             color_discrete_map=custom_colors,  # Aplicando a paleta de cores personalizada
             barmode='group',
             text='Avaliação',  # Adicionando os rótulos nas barras
             labels={"Ano Turma": "Ano", "Média (%)": "Média (%)"},
             title="Média Geral das Avaliações por Ano")

# Removendo o quadro de legenda e ajustando o layout dos rótulos
fig4.update_layout(showlegend=False)
fig4.update_traces(textposition='outside')  # Posicionando o texto acima das barras

############# fim Grafico para visualizar media geral das avaliações dos cursos por ano #########################################

st.markdown('# Visão Geral')
st.divider()

espaco_esquerda, col1, col2, espaco_direita = st.columns([1.5, 2, 2, 1.5])  # Ajuste as proporções conforme necessário
#col1.metric('Total de Aprovados por curso',total_aprovados_geral)
col1.markdown(f"""
    <div style="
        background-color: #8D0333; 
        padding: 2px; 
        border-radius: 10px; 
        text-align: center;
        color: white;
        font-size: 15px;
        width: auto;
    ">
        <h3 style="margin: 0; color: white;">Total de Aprovados por Curso</h3>
        <p style="font-size: 40px; margin: 0; font-weight: bold;">{total_aprovados_geral}</p>
    </div>
    """, unsafe_allow_html=True)


col2.markdown(f"""
    <div style="
        background-color: #8D0333; 
        padding: 2px; 
        border-radius: 10px; 
        text-align: center;
        color: white;
        font-size: 15px;
        width: auto;
    ">
        <h3 style="margin: 0; color: white;">Total de Avaliações Realizadas</h3>
        <p style="font-size: 40px; margin: 0; font-weight: bold;">{total_avaliacoes_geral}</p>
    </div>
    """, unsafe_allow_html=True)

#st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
#st.sidebar.image("img/ufma.png", use_column_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

# Mostrar o gráfico de pizza sobre media
col2.plotly_chart(fig)

# Exibir o gráfico
col1.plotly_chart(fig2)

###################################
# Mostrar o gráfico de pizza sobre media
col2.plotly_chart(fig3)

# Exibir o gráfico
col1.plotly_chart(fig4)

###################################


# Aplicar a limpeza nos comentários
df_comentarios['Comentario_limpo'] = df_comentarios['Comentário'].apply(limpar_texto)

# Unir todos os comentários em um único texto
todos_comentarios = ' '.join(df_comentarios['Comentario_limpo'])

# Gerar a nuvem de palavras
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(todos_comentarios)

st.markdown("<br>", unsafe_allow_html=True)
# Dividindo em duas colunas para exibir os gráficos
col1, col2 = st.columns(2)

# Exibir a nuvem de palavras
with col1:
    st.markdown("### Nuvem de Palavras dos Comentários")
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Classificar os comentários como Positivo, Negativo ou Neutro
def classificar_comentario(comentario):
    palavras_positivas = ["excelente", "ótimo", "bom", "parabéns", "maravilhoso", "incrível", "satisfatório","boa","agregaram","excelentes"]
    palavras_negativas = ["ruim", "péssimo", "não gostei", "horrível", "insatisfatório", "fraco", "problema"]
    palavras_neutras = ["ok", "regular", "aceitável", "mediano", "neutro"]
    
    comentario = comentario.lower()
    if any(palavra in comentario for palavra in palavras_positivas):
        return "Positivo"
    elif any(palavra in comentario for palavra in palavras_negativas):
        return "Negativo"
    elif any(palavra in comentario for palavra in palavras_neutras):
        return "Neutro"
    else:
        return "Neutro"

# Aplicar a classificação
df_comentarios['Classificacao_Regras'] = df_comentarios['Comentário'].apply(classificar_comentario)

# Contar a quantidade de classificações
classificacao_counts = df_comentarios['Classificacao_Regras'].value_counts().reset_index()
classificacao_counts.columns = ['Classificacao', 'Contagem']

# Criar o gráfico de classificação com Plotly
fig_classificacao = px.bar(classificacao_counts, 
                          x='Classificacao', 
                          y='Contagem', 
                          #title='Distribuição de Classificações dos Comentários (Regras)',
                          labels={'Classificacao': 'Classificação', 'Contagem': 'Número de Comentários'},
                          color='Classificacao', 
                          color_discrete_map={'Neutro': '#FEC84D', 'Positivo': '#0AB0AB', 'Negativo': '#FF5733'})

fig_classificacao.update_layout(
    xaxis_title="Classificação",
    yaxis_title="Número de Comentários",
    showlegend=False
)

# Exibir o gráfico de classificação
with col2:
    st.markdown("### Classificação dos Comentários")
    st.plotly_chart(fig_classificacao, use_container_width=True)

# Rodapé
#st.markdown("<p style='text-align: center; color: grey;'>Desenvolvido pela equipe da Divisão de Capacitação e Desenvolvimento da UFMA</p>", unsafe_allow_html=True)
#st.markdown("<p style='text-align: right; color: grey;'>Última atualização: 20/09/2024</p>", unsafe_allow_html=True)


st.markdown("<div style='position: fixed; bottom: 0; width: 100%; text-align: center; color: grey;'>Desenvolvido pela equipe da Divisão de Capacitação e Desenvolvimento da UFMA</div>", unsafe_allow_html=True)
st.markdown("<div style='position: fixed; bottom: 0; right: 0; color: grey;'>Última atualização: 20/09/2024</div>", unsafe_allow_html=True)