from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px

# Configurar a página
st.set_page_config(page_title="Dashboard Interativo", layout="wide")

# Importando os dataframes
df_geral = pd.read_excel('pages/df_analise.xlsx', decimal='.')
df_comentarios = pd.read_excel('pages/df_comentarios.xlsx', decimal='.')

# Título e Divisor
st.markdown('# Ranking')
st.divider()

# Selecionar o tipo de ranking
tipo_ranking = st.radio("Selecione o tipo de ranking:", ("Ranking de Professor", "Ranking de Turma"))

# Selecionar o ano
anos_disponiveis = df_geral['Ano Turma'].unique()
ano_selecionado = st.selectbox("Selecione o Ano", sorted(anos_disponiveis))

# Filtrar os dados com base no tipo de ranking e ano selecionado
if tipo_ranking == "Ranking de Professor":
    # Filtrar os dados pela categoria "Avaliação do(s) Instrutor(es)" e ano
    dados_instrutores = df_geral[(df_geral['Categoria'] == "Avaliação do(s) Instrutor(es)") & (df_geral['Ano Turma'] == ano_selecionado)]
    
    # Agrupar os dados por 'Instrutor' e calcular a média das avaliações
    ranking_instrutores = dados_instrutores.groupby(['Instrutor', 'Turma'])[['Ótimo (%)', 'Bom (%)', 'Regular (%)', 'Fraco (%)']].mean()
    
    # Calcular uma média ponderada para criar o ranking
    ranking_instrutores['Média Avaliação'] = (
        ranking_instrutores['Ótimo (%)'] * 4 + 
        ranking_instrutores['Bom (%)'] * 3 + 
        ranking_instrutores['Regular (%)'] * 2 + 
        ranking_instrutores['Fraco (%)'] * 1
    ) / 4
    
    # Ordenar o ranking pela média da avaliação (decrescente)
    ranking_instrutores = ranking_instrutores.sort_values(by='Média Avaliação', ascending=False).reset_index()
    
    # Adicionar a coluna de classificação
    ranking_instrutores['Colocação'] = ranking_instrutores['Média Avaliação'].rank(ascending=False).astype(int)
    
    # Selecionar as colunas para exibição
    ranking_final = ranking_instrutores[['Colocação', 'Instrutor', 'Turma', 'Média Avaliação']]
    
    # Exibir o DataFrame
    st.markdown("### Ranking de Professores")
    st.dataframe(ranking_final.style.format({"Média Avaliação": "{:.2f}"}), use_container_width=True)

elif tipo_ranking == "Ranking de Turma":
    # Filtrar os dados pelo ano selecionado
    comparativo_aprovados = df_geral[df_geral['Ano Turma'] == ano_selecionado].groupby('Turma').agg({
        'Total_Avaliacao': 'sum', 
        'Aprovados': 'sum'
    }).reset_index()
    
    # Calcular a porcentagem de avaliações
    comparativo_aprovados['Percentual_Avaliação'] = (comparativo_aprovados['Total_Avaliacao'] / comparativo_aprovados['Aprovados']) * 100

    # Normalizar o número de avaliações (escala de 0 a 1)
    comparativo_aprovados['Normalizado_Avaliacoes'] = (
        (comparativo_aprovados['Total_Avaliacao'] - comparativo_aprovados['Total_Avaliacao'].min()) /
        (comparativo_aprovados['Total_Avaliacao'].max() - comparativo_aprovados['Total_Avaliacao'].min())
    )

    # Calcular a pontuação final (peso de 50% para média e 50% para número de avaliações normalizado)
    comparativo_aprovados['Score'] = (
        0.5 * comparativo_aprovados['Percentual_Avaliação'] +
        0.5 * comparativo_aprovados['Normalizado_Avaliacoes'] * 100  # Convertido para escala de porcentagem
    )

    # Ordenar os cursos pelo score
    ranking_cursos = comparativo_aprovados[['Turma', 'Score', 'Total_Avaliacao', 'Percentual_Avaliação']].sort_values(by='Score', ascending=False).reset_index(drop=True)
    
    # Adicionar a coluna de classificação
    ranking_cursos['Colocação'] = ranking_cursos['Score'].rank(ascending=False).astype(int)
    
    # Exibir o DataFrame
    st.markdown("### Ranking de Turmas")
    st.dataframe(ranking_cursos[['Colocação', 'Turma', 'Score', 'Total_Avaliacao', 'Percentual_Avaliação']].style.format({"Score": "{:.2f}", "Percentual_Avaliação": "{:.2f}"}), use_container_width=True)

# Rodapé
st.markdown("<div style='position: fixed; bottom: 0; width: 100%; text-align: center; color: grey;'>Desenvolvido pela equipe da Divisão de Capacitação e Desenvolvimento da UFMA</div>", unsafe_allow_html=True)
st.markdown("<div style='position: fixed; bottom: 0; right: 0; color: grey;'>Última atualização: 20/09/2024</div>", unsafe_allow_html=True)
