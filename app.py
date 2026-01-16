import streamlit as st
import pandas as pd
import plotly.express as px
# import os
# from dotenv import load_dotenv
import jira_report

# Configuración de la página
st.set_page_config(
    page_title="Reporte de Horas Jira",
    page_icon="⏱️",
    layout="wide"
)

# Cargar variables de entorno
# load_dotenv()

st.title("⏱️ Reporte de Horas Jira")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    
    # Valores por defecto (Sin .env)
    
    jira_url = st.text_input("Jira URL", value="", placeholder="")
    # Simplify Auth: Just Token (PAT)
    jira_token = st.text_input("Personal Access Token", value="", type="password", help="Tu Token Personal (PAT).")
    
    st.markdown("---")
    st.subheader("Filtros")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        project_key = st.text_input("Clave Proyecto", value="", help="Ej: MOV, PROJ")
    with col_f2:
        author_name = st.text_input("Usuario (Autor)", value="", help="Tu nombre de usuario en Jira")
    
    days = st.slider("Días a analizar", min_value=1, max_value=90, value=30)
    
    st.markdown("---")
    st.caption("v1.0.1 - Filtrado Autor Manual")

if st.button("Generar Reporte", type="primary"):
    if not jira_url or not jira_token or not project_key or not author_name:
        st.error("Faltan datos. URL, Token, Proyecto y Usuario son obligatorios.")
    else:
        try:
            with st.spinner(f"Buscando worklogs de '{author_name}' en proyecto '{project_key}'..."):
                # Conectar (Solo Token -> PAT)
                client = jira_report.JiraAPIClient(url=jira_url, token=jira_token)
                
                # Obtener datos (Lista de diccionarios detallada)
                worklogs_data = jira_report.get_worklogs_filtered(
                    client, 
                    project_key=project_key, 
                    author_name=author_name, 
                    days=days
                )
                
            if not worklogs_data:
                st.warning("No se encontraron horas registradas en el periodo seleccionado para ese usuario.")
            else:
                # Procesar datos
                df = pd.DataFrame(worklogs_data)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values(by=['date', 'key'], ascending=False)
                
                total_hours = df['hours'].sum()
                
                # Métricas principales
                st.metric(label="Total Horas Trabajadas", value=f"{total_hours:.2f} h")
                
                # Gráfico: Agrupar por fecha
                df_daily = df.groupby('date')['hours'].sum().reset_index()
                
                st.subheader("Gráfico Diario")
                fig = px.bar(df_daily, x='date', y='hours', title=f"Horas por día (Últimos {days} días)")
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Detalle de Tareas")
                # Formatear para visualización
                df_display = df.copy()
                df_display['Fecha'] = df_display['date'].dt.strftime('%Y-%m-%d')
                df_display = df_display[['Fecha', 'key', 'type', 'summary', 'hours']]
                df_display.columns = ['Fecha', 'Clave', 'Tipo', 'Título', 'Horas']
                
                st.dataframe(
                    df_display, 
                    hide_index=True, 
                    use_container_width=True,
                    column_config={
                        "Horas": st.column_config.NumberColumn(format="%.2f h")
                    }
                )
                    
        except Exception as e:
            err_msg = str(e)
            if "401" in err_msg:
                 st.error("Error de Autenticación (401). Verifica tu Token. El token puede haber expirado.")
            elif "404" in err_msg:
                 st.error("Error 404. URL no encontrada.")
            else:
                 st.error(f"Error: {err_msg}")
