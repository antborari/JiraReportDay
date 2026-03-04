import streamlit as st
import pandas as pd
import plotly.express as px

def render_daily_chart(df_chart: pd.DataFrame, title: str):
    """Gráfico de barras diario para un usuario."""
    df_grp = df_chart.groupby('date')['hours'].sum().reset_index().sort_values('date')
    
    fig = px.bar(
        df_grp, 
        x='date', 
        y='hours', 
        title=title,
        text_auto='.1f',
        color_discrete_sequence=['#4C78A8']
    )
    
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Horas",
        xaxis_tickformat='%d/%m',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(tickangle=-45)
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    st.plotly_chart(fig, use_container_width=True)
