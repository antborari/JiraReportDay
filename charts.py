import streamlit as st
import pandas as pd
import plotly.express as px


def render_pie_chart(df_user_summary: pd.DataFrame):
    """Gráfico de torta con distribución de horas por usuario."""
    fig = px.pie(
        df_user_summary, 
        values='Horas', 
        names='Usuario', 
        title="Distribución de Horas",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(df_user_summary: pd.DataFrame):
    """Gráfico de barras con total de horas por usuario."""
    fig = px.bar(
        df_user_summary, 
        x='Usuario', 
        y='Horas', 
        color='Usuario',
        title="Total Horas por Usuario", 
        text_auto='.1f',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20), showlegend=False, xaxis_title="", yaxis_title="Horas")
    st.plotly_chart(fig, use_container_width=True)


def render_daily_chart(df_chart: pd.DataFrame, title: str):
    """Gráfico de barras diario para todos los usuarios."""
    df_grp = df_chart.sort_values('date')
    
    fig = px.bar(
        df_grp, 
        x='date', 
        y='hours', 
        color='usuario',
        title=title,
        text_auto='.1f',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Horas",
        xaxis_tickformat='%d/%m',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(tickangle=-45),
        barmode='group'
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    st.plotly_chart(fig, use_container_width=True)
