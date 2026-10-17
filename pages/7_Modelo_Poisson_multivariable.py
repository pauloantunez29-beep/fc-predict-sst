import streamlit as st
import pandas as pd, numpy as np, json
import plotly.express as px
from pathlib import Path
P=Path(__file__).resolve().parent.parent
st.title("🧪 Modelo Poisson multivariable · demostración 7.1")
st.caption("Fuente metodológica: conjunto de datos de prueba para el ajuste multivariable; la serie histórica se presenta por separado.")
df=pd.read_csv(P/"base_prueba_cuadrillas_multivariada.csv")
coef=pd.read_csv(P/"coeficientes_poisson_prueba.csv").set_index("variable")
metrics=json.loads((P/"metricas_validacion_prueba.json").read_text(encoding="utf8"))
c1,c2,c3,c4=st.columns(4)
c1.metric("Registros de prueba",metrics["n_registros"])
c2.metric("Accidentes generados",metrics["accidentes_generados"])
c3.metric("Incidentes generados",metrics["incidentes_generados"])
c4.metric("MAE 2025 (prueba)",f'{metrics["mae_prueba"]:.3f}')
st.subheader("Multiplicadores estimados en la base de demostración")
st.caption("Coeficientes estimados con la base de prueba; interpretación asociativa, no causal.")
st.dataframe(coef.reset_index().round(4),hide_index=True,use_container_width=True)
st.caption("Multiplicador = exp(coeficiente). El intercepto no es un factor preventivo; representa la tasa de referencia por HHT.")
st.subheader("Escenario de una cuadrilla")
a,b,c=st.columns(3)
with a:
 n=st.number_input("Trabajadores",1,30,10);dias=st.number_input("Días",1,31,22);horas=st.number_input("Horas diarias",1.,12.,8.)
with b:
 acto=int(st.checkbox("Acto subestándar"));cond=int(st.checkbox("Condición subestándar"));preuso=int(st.checkbox("Inspección preuso conforme",value=True))
with c:
 control=int(st.checkbox("Controles críticos conformes",value=True));iperc=st.selectbox("IPERC nivel",[1,2,3],index=1);exp=st.number_input("Experiencia media (años)",0.,40.,6.)
inputs={"const":1,"acto_subestandar":acto,"condicion_subestandar":cond,"controles_criticos_conformes":control,"iperc_nivel":iperc,"experiencia_media_anios":exp,"preuso_conforme":preuso}
hht=n*dias*horas
lam=float(np.exp(np.log(hht)+sum(float(coef.loc[k,"coeficiente"])*v for k,v in inputs.items())))
p=1-np.exp(-lam)
st.metric("Accidentes esperados (escenario)",f"{lam:.3f}")
base_inputs=dict(inputs);base_inputs.update({"acto_subestandar":0,"condicion_subestandar":0,"controles_criticos_conformes":1,"preuso_conforme":1})
lam_control=float(np.exp(np.log(hht)+sum(float(coef.loc[k,"coeficiente"])*v for k,v in base_inputs.items())))
p_control=1-np.exp(-lam_control)
st.subheader("Comparación de decisiones preventivas")
comp=pd.DataFrame({"Escenario":["Situación ingresada","Actos/condiciones corregidos y controles verificados"],"Probabilidad de al menos un accidente (%)":[100*p,100*p_control]})
st.plotly_chart(px.bar(comp,x="Escenario",y="Probabilidad de al menos un accidente (%)",text_auto=".2f"),use_container_width=True)
st.caption("Comparación de escenarios del modelo; no representa una estimación causal del efecto de las intervenciones.")
if acto or cond or not control or not preuso:
 st.warning("Priorizar eliminación, sustitución y controles de ingeniería: retirar equipos defectuosos, instalar guardas y extracción localizada, utilizar sistemas de sujeción mecánica y verificar bloqueo de energías. Aplicar las medidas específicas según el IPERC de la actividad.")
registro={"trabajadores":n,"dias":dias,"horas_diarias":horas,"hht":hht,"acto_subestandar":acto,"condicion_subestandar":cond,"preuso_conforme":preuso,"controles_criticos_conformes":control,"iperc_nivel":iperc,"experiencia_media_anios":exp,"accidentes_esperados":lam,"probabilidad_accidente":p,"probabilidad_escenario_corregido":p_control,"origen":"demostracion_7_0"}
st.download_button("Descargar evidencia del escenario (CSV)",pd.DataFrame([registro]).to_csv(index=False).encode("utf-8-sig"),file_name="evidencia_escenario_7_0.csv",mime="text/csv")
st.metric("Probabilidad de ≥1 accidente (escenario)",f"{100*p:.2f}%")
if not control:
 st.error("Control crítico ausente: revisar IPERC y detener la tarea cuando corresponda, independientemente del pronóstico.")
st.subheader("Validación temporal interna")
st.write("Entrenamiento: 2021–2024. Evaluación temporal: 2025. Fuente: base de prueba.")
st.write({k:round(v,4) if isinstance(v,float) else v for k,v in metrics.items() if k in ["mae_prueba","rmse_prueba","dispersion_pearson","media_observada_prueba","media_predicha_prueba"]})
st.subheader("Exploración de la base")
y=st.selectbox("Año",["Todos"]+sorted(df.anio.unique().tolist()))
sub=df if y=="Todos" else df[df.anio==y]
st.dataframe(sub,hide_index=True,use_container_width=True)
st.download_button("Descargar base generada",df.to_csv(index=False).encode("utf-8-sig"),file_name="base_prueba_cuadrillas_multivariada.csv",mime="text/csv")
