import streamlit as st
import pandas as pd
from pathlib import Path
st.title("Exploración multivariable — casos de prueba")
st.caption("Conjunto de datos de prueba para el análisis exploratorio.")
file=Path(__file__).resolve().parents[1]/"eventos_prueba_multivariables.csv"
df=pd.read_csv(file)
tipo=st.multiselect("Tipo de evento",sorted(df.tipo_evento.unique()),default=sorted(df.tipo_evento.unique()))
acts=st.multiselect("Actividad",sorted(df.actividad.unique()),default=sorted(df.actividad.unique()))
f=df[df.tipo_evento.isin(tipo)&df.actividad.isin(acts)]
c1,c2,c3=st.columns(3)
c1.metric("Eventos de prueba",len(f));c2.metric("Accidentes de prueba",(f.tipo_evento=="Accidente incapacitante").sum());c3.metric("Días perdidos de prueba",int(f.dias_perdidos.sum()))
st.subheader("Distribución por año y tipo")
st.bar_chart(pd.crosstab(f.anio,f.tipo_evento))
st.subheader("Edad y experiencia por tipo de evento")
st.dataframe(f.groupby("tipo_evento")[["edad","experiencia_anios","acto_subestandar","condicion_subestandar"]].mean().round(2),use_container_width=True)
st.subheader("Registros de prueba")
st.dataframe(f,use_container_width=True,hide_index=True)
st.download_button("Exportar selección CSV",f.to_csv(index=False).encode("utf-8-sig"),"seleccion_eventos_prueba.csv","text/csv")
st.caption("Resultados exploratorios de la base de prueba; no se interpretan como relaciones causales.")