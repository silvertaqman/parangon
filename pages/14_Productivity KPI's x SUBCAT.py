import streamlit as st
import plotly.express as px
from utils import backend

plotly_palette = backend.plotly_palette
if not st.session_state.get("data_ready", False):
    st.error("Los datos no están disponibles. Completa el proceso de ingreso de datos para acceder a esta página.")
    st.stop()
df_subcat = st.session_state["total_scorecard_subcat"]


df_subcat = df_subcat.loc[[
    "Rotación",
    "Días de inventario - 250 días al año",
    "Días de inventario - 360 días al año",
    "Meses de inventario",
    "GMROI - Gross Margin Return on Inventory"
]]

df_subcat_styled = df_subcat.copy()
df_subcat_styled.iloc[[1,2]] = df_subcat_styled.iloc[[1,2]].applymap(lambda x: f"{x:.0f}")
df_subcat_styled.iloc[[0,3]] = df_subcat_styled.iloc[[0,3]].applymap(lambda x: f"{x:.2f}")
df_subcat_styled.iloc[[4]] = df_subcat_styled.iloc[[4]].applymap(lambda x: f"{x:.2%}")

df_subcat_styled = backend.style_df(df_subcat_styled,colo1="orange", color2="lawngreen")


st.dataframe(df_subcat_styled, use_container_width=True)

sorted = st.checkbox("Ordenar")

col1, col2, col3 = st.columns([1/3, 1/3, 1/3])
with col1:
    df_to_plot = df_subcat.loc["Rotación"]
    if sorted:
        df_to_plot = df_to_plot.sort_values(ascending=False)
    total = df_to_plot["Costo Totales"]
    df_to_plot.drop("Costo Totales", inplace=True)
    fig = px.bar(
        x=df_to_plot.index,
        y=df_to_plot.values,
        title=f"{df_to_plot.name} <br>Costo Total: <span style='color:red;'>{total:.2f}</span>",
        labels={"x": "", "y": ""}
    )
    fig.update_traces(
        marker_color=plotly_palette[0],
        texttemplate='%{value:,.2f}',
        textposition='outside',
        width=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    df_to_plot = df_subcat.loc["Días de inventario - 250 días al año"]
    if sorted:
        df_to_plot = df_to_plot.sort_values(ascending=False)
    total = df_to_plot["Costo Totales"]
    df_to_plot.drop("Costo Totales", inplace=True)
    fig = px.bar(
        x=df_to_plot.index,
        y=df_to_plot.values,
        title=f"{df_to_plot.name} <br>Costo Total: <span style='color:red;'>{total:,.0f}</span>",
        labels={"x": "", "y": ""}
    )
    fig.update_traces(
        marker_color=plotly_palette[1],
        texttemplate='%{value:,.0f}',
        textposition='outside',
        width=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    df_to_plot = df_subcat.loc["Días de inventario - 360 días al año"]
    if sorted:
        df_to_plot = df_to_plot.sort_values(ascending=False)
    total = df_to_plot["Costo Totales"]
    df_to_plot.drop("Costo Totales", inplace=True)
    fig = px.bar(
        x=df_to_plot.index,
        y=df_to_plot.values,
        title=f"{df_to_plot.name} <br>Costo Total: <span style='color:red;'>{total:,.0f}</span>",
        labels={"x": "", "y": ""}
    )
    fig.update_traces(
        marker_color=plotly_palette[2],
        texttemplate='%{value:,.0f}',
        textposition='outside',
        width=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns([1/3, 1/3, 1/3])
with col1:
    df_to_plot = df_subcat.loc["Meses de inventario"]
    if sorted:
        df_to_plot = df_to_plot.sort_values(ascending=False)
    total = df_to_plot["Costo Totales"]
    df_to_plot.drop("Costo Totales", inplace=True)
    fig = px.bar(
        x=df_to_plot.index,
        y=df_to_plot.values,
        title=f"{df_to_plot.name} <br>Costo Total: <span style='color:red;'>{total:,.2f}</span>",
        labels={"x": "", "y": ""}
    )
    fig.update_traces(
        marker_color=plotly_palette[3],
        texttemplate='%{value:,.2f}',
        textposition='outside',
        width=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    df_to_plot = df_subcat.loc["GMROI - Gross Margin Return on Inventory"]
    if sorted:
        df_to_plot = df_to_plot.sort_values(ascending=False)
    total = df_to_plot["Costo Totales"]
    df_to_plot.drop("Costo Totales", inplace=True)
    fig = px.bar(
        x=df_to_plot.index,
        y=df_to_plot.values,
        title=f"{df_to_plot.name} <br>Costo Total: <span style='color:red;'>{total:.2%}</span>" ,
        labels={"x": "", "y": ""}
    )
    fig.update_layout(
        yaxis_tickformat='.0%'  # Formato de moneda para el eje y
    )
    fig.update_traces(
        marker_color=plotly_palette[4],
        texttemplate='%{value:.1%}',
        textposition='outside',
        width=0.6
    )
    st.plotly_chart(fig, use_container_width=True)