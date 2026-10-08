import streamlit as st
import pandas as pd, numpy as np, joblib
import plotly.express as px
from pathlib import Path
st.set_page_config(page_title="FC PREDICT SST 6.6",page_icon="🦺",layout="wide")
P=Path(__file__).parent
hist=pd.read_csv(P/'historico_real.csv')
hist['IA']=hist['IF']*hist['IS']/1000
data=pd.read_csv(P/'escenarios_sinteticos.csv')
model_acc=joblib.load(P/'accidente_simulado.joblib')
model_inc=joblib.load(P/'incidente_simulado.joblib')
ACTOS=['Omitir inspección preuso','No utilizar EPP','Retirar guardas de seguridad','Operar sin autorización','Trabajar sin permiso de trabajo','No asegurar carga suspendida','Uso inadecuado de herramientas','Ingresar a zona restringida','Omitir bloqueo y etiquetado','Adoptar postura insegura','Improvisar plataformas','No respetar señalización','Soldar sin protección facial','Manipular cargas sin apoyo','Realizar maniobra sin señalero']
COND=['Herramienta o equipo defectuoso','Guardas de seguridad ausentes','Cables eléctricos deteriorados','Falta de ventilación o extracción','Área de trabajo desordenada','Superficie resbaladiza','Iluminación insuficiente','Carga suspendida sin delimitación','Ausencia de línea de vida','Andamio o escalera no conforme','Exposición a ruido elevado','Proyección de partículas sin barrera','Materiales apilados inestablemente','Extintor no disponible','Temperatura ambiental elevada','Señalización insuficiente','Equipo de izaje sin inspección','Espacio reducido sin control']
ACTIVIDADES=['Soldadura','Corte y esmerilado','Montaje de estructuras','Manipulación de perfiles','Trabajo en altura','Izaje de materiales','Mantenimiento de equipos']
MESES=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

NOMBRES={'anio':'Año','mes':'Mes','hht':'Horas-hombre trabajadas','accidentes':'Accidentes incapacitantes','dias_perdidos':'Días perdidos','accidentes_incapacitantes':'Accidentes incapacitantes','accidentes_no_incapacitantes':'Accidentes no incapacitantes','incidentes':'Incidentes','edad':'Edad (años)','experiencia_anios':'Experiencia (años)','actividad':'Actividad','iperc':'Nivel IPERC','acto_subestandar':'Acto subestándar','condicion_subestandar':'Condición subestándar','epp_conforme':'EPP conforme','preuso_conforme':'Inspección preuso conforme','controles_conformes':'Controles críticos conformes','temporada_ilustrativa':'Temporada','evento':'Evento','accidente_simulado':'Accidente','incidente_simulado':'Incidente'}
reg_inc=pd.read_csv(P/'registro_incidentes.csv')
reg_mensual=pd.read_csv(P/'registro_mensual_practica.csv')
reg_acc=pd.read_csv(P/'fechas_accidentes_escenario.csv',encoding='utf-8-sig')
def tabla_mensual():
 t=reg_mensual.copy()
 t['mes']=t.mes.map(lambda m:MESES[int(m)-1])
 return t.rename(columns=NOMBRES)

st.markdown("""<style>
.stApp{background:linear-gradient(155deg,#f1f6fc,#fff 55%,#e9f3fa)}
.block-container{padding-top:1.5rem;max-width:1500px}
[data-testid="stMetric"]{background:white;padding:18px;border-radius:14px;border:1px solid #dce7f2;box-shadow:0 5px 18px rgba(15,45,75,.06)}
[data-testid="stMetricValue"]{color:#12395b;font-weight:800}
h1,h2,h3{color:#173f62!important}
div.stButton>button[kind="primary"]{background:linear-gradient(100deg,#0a5984,#1c89ac);border-radius:12px;font-weight:750}
</style>""",unsafe_allow_html=True)
st.title('🦺 FC PREDICT SST 6.6')
st.markdown('### Centro de inteligencia preventiva · FC Estructuras E.I.R.L.')
st.caption('Pronóstico mensual por cuadrilla · Antecedentes 2021–2025 · Gestión preventiva')
st.markdown('**Categorías:** accidente de trabajo = lesión laboral; accidente incapacitante = accidente con incapacidad y días perdidos; incidente = suceso sin lesión incapacitante. No deben sumarse como categorías independientes.')
t0,t1,t2,t3,t4=st.tabs(['🏠 Dashboard ejecutivo','🎯 Pronóstico por cuadrilla','📊 Antecedentes 2021–2025','📅 Análisis por mes y año','📘 Modelo y datos'])
with t0:
 st.subheader('Panel ejecutivo de seguridad · 2021–2025')
 c1,c2,c3,c4=st.columns(4)
 c1.metric('Accidentes incapacitantes',int(hist.accidentes.sum()))
 c2.metric('Días perdidos',int(hist.dias_perdidos.sum()))
 c3.metric('Horas-hombre trabajadas',f'{int(hist.hht.sum()):,}')
 c4.metric('Índice de accidentabilidad',f"{(hist.accidentes.sum()*1e6/hist.hht.sum())*(hist.dias_perdidos.sum()*1e6/hist.hht.sum())/1000:.2f}")
 a,b=st.columns(2)
 with a:
  st.plotly_chart(px.bar(hist,x='anio',y='accidentes',labels={'anio':'Año','accidentes':'Accidentes incapacitantes'},text_auto=True,title='Accidentes incapacitantes por año',color_discrete_sequence=['#1c729d']),use_container_width=True)
 with b:
  st.plotly_chart(px.bar(hist,x='anio',y='dias_perdidos',labels={'anio':'Año','dias_perdidos':'Días perdidos'},text_auto=True,title='Días perdidos por año',color_discrete_sequence=['#dd8951']),use_container_width=True)
 st.markdown('#### Evolución de los tres índices de SST')
 aa,bb,cc=st.columns(3)
 for column,container,title,unit in [('IF',aa,'Índice de frecuencia','Accidentes / millón HHT'),('IS',bb,'Índice de severidad','Días perdidos / millón HHT'),('IA',cc,'Índice de accidentabilidad','IF × IS / 1000')]:
  with container:
   fig=px.line(hist,x='anio',y=column,markers=True,title=title)
   fig.update_traces(mode='lines+markers+text',text=hist[column].round(2),textposition='top center',line=dict(width=3),marker=dict(size=9))
   fig.update_layout(xaxis_title='Año',yaxis_title=unit,height=330,margin=dict(l=15,r=15,t=55,b=20))
   st.plotly_chart(fig,use_container_width=True)
 st.caption('Los índices son indicadores históricos; no equivalen a la probabilidad futura de accidente. Los incidentes de desarrollo se identifican en la sección de análisis.')
with t1:
 st.subheader('Pronóstico mensual de accidentes e incidentes')
 c1,c2,c3=st.columns(3)
 with c1:
  year=st.selectbox('Año del pronóstico',[2026],index=0)
  month=st.selectbox('Mes del pronóstico',range(1,13),index=9,format_func=lambda x:MESES[x-1])
 with c2:
  actividad=st.selectbox('Actividad principal',ACTIVIDADES)
  n=st.number_input('Cantidad de trabajadores',1,30,10)
 with c3:
  dias=st.number_input('Días de trabajo durante el mes',1,31,22)
  horas=st.number_input('Horas por trabajador y día',1.0,12.0,8.0,step=.5)
 st.markdown('#### Antecedentes del mes seleccionado (2021–2025)')
 comparacion=tabla_mensual()
 comparacion=comparacion[comparacion['Mes']==MESES[month-1]]
 st.dataframe(comparacion[['Año','Mes','Accidentes incapacitantes','Accidentes no incapacitantes','Incidentes']],hide_index=True,use_container_width=True)
 st.markdown('#### Características de la cuadrilla')
 # Los campos numéricos son editables con teclado y botones +/-.
 perfiles=[(21,1),(24,2),(28,4),(32,7),(39,12),(45,18),(26,3),(35,9),(51,23),(30,6),(23,2),(42,15),(37,11),(29,5),(48,20)]
 if 'cuadrilla_perfiles' not in st.session_state:
  st.session_state.cuadrilla_perfiles={i:{'Edad (años)':perfiles[i%len(perfiles)][0],'Experiencia (años)':perfiles[i%len(perfiles)][1]} for i in range(30)}
 st.caption('Modifica directamente cada número. Los cambios se conservan al variar la cantidad de trabajadores.')
 registros=[]
 for i in range(n):
  st.markdown(f'**Trabajador {i+1}**')
  ca,cb=st.columns(2)
  with ca:
   edad=st.number_input(f'Edad del trabajador {i+1} (años)',min_value=18,max_value=70,value=int(st.session_state.cuadrilla_perfiles[i]['Edad (años)']),step=1,key=f'edad_trab_{i}')
  with cb:
   exp=st.number_input(f'Experiencia del trabajador {i+1} (años)',min_value=0,max_value=50,value=int(st.session_state.cuadrilla_perfiles[i]['Experiencia (años)']),step=1,key=f'exp_trab_{i}')
  st.session_state.cuadrilla_perfiles[i]={'Edad (años)':edad,'Experiencia (años)':exp}
  registros.append({'Trabajador':f'Trabajador {i+1}','Edad (años)':edad,'Experiencia (años)':exp})
 edited=pd.DataFrame(registros)
 st.markdown('**Resumen de la cuadrilla**')
 st.dataframe(edited,hide_index=True,use_container_width=True)
 a,b=st.columns(2)
 with a:
  iperc=st.select_slider('Nivel IPERC de la actividad',options=[1,2,3],value=2,format_func=lambda x:{1:'Bajo',2:'Medio',3:'Alto'}[x])
  acts=st.multiselect('Actos subestándares identificados',ACTOS)
 with b:
  conds=st.multiselect('Condiciones subestándares identificadas',COND)
  epp=st.checkbox('EPP conforme',value=True)
  preuso=st.checkbox('Inspección preuso conforme',value=True)
  controls=st.checkbox('Controles críticos implementados',value=True)
 if st.button('🔎 CALCULAR PRONÓSTICO MENSUAL',type='primary'):
  if edited[['Edad (años)','Experiencia (años)']].isna().any().any():
   st.error('Completa edad y experiencia de todos los trabajadores.')
  else:
   # Historical annual accident frequency, with monthly exposure of the evaluated crew.
   hht=float(n*dias*horas)
   tasa=float(hist.accidentes.sum()/hist.hht.sum())
   avg_age=float(edited['Edad (años)'].mean()); avg_exp=float(edited['Experiencia (años)'].mean())
   # Preventive scenario factors (not coefficients fitted to company accident records).
   f_iperc={1:.8,2:1.0,3:1.35}[iperc]
   f_act=min(1.0+.18*len(acts),1.9)
   f_cond=min(1.0+.20*len(conds),2.0)
   f_controls=(1.0 if controls else 1.55)*(1.0 if epp else 1.25)*(1.0 if preuso else 1.20)
   f_inc=1.0  # No se solicita un antecedente que no conste en la base histórica.
   f_exp=1.15 if avg_exp<2 else (1.05 if avg_exp<5 else 1.0)
   factor=f_iperc*f_act*f_cond*f_controls*f_inc*f_exp
   expected=tasa*hht*factor
   p=1-np.exp(-expected)
   baseline=1-np.exp(-tasa*hht)
   # Incident forecast based on the separate development dataset; not a company-validated probability.
   incidentes_practica=pd.read_csv(P/'registro_incidentes.csv')
   tasa_inc=len(incidentes_practica)/float(hist.hht.sum())
   p_inc=1-np.exp(-tasa_inc*hht*factor)
   st.subheader(f'Resultado: {MESES[month-1]} de {year} — {actividad}')
   st.markdown('### Resultado del pronóstico mensual')
   c1,c2,c3=st.columns(3)
   c1.metric('Accidente incapacitante · ≥1 en el mes',f'{p*100:.2f} %')
   c2.metric('Incidente · ≥1 en el mes (modelo de desarrollo)',f'{p_inc*100:.2f} %')
   c3.metric('Exposición de la cuadrilla',f'{hht:,.0f} HHT')
   st.info(f"📌 **Lectura del resultado:** Para {n} trabajadores de **{actividad}**, durante **{MESES[month-1]} de {year}**, el sistema estima **{p*100:.2f} %** de probabilidad de que ocurra **al menos un accidente incapacitante** en la cuadrilla. La estimación orientativa de **al menos un incidente** es **{p_inc*100:.2f} %**. Ningún porcentaje indica cuántos trabajadores sufrirán un evento.")
   st.caption('Los porcentajes representan escenarios de planificación calculados con una frecuencia histórica y ajustes preventivos. No son predicciones validadas individualmente. El cálculo de incidentes utiliza registros de desarrollo, no partes empresariales confirmados.')
   if p >= 0.15:
    st.warning('La probabilidad mensual de accidente supera el 15 % en el escenario ingresado: priorizar revisión preventiva.')
   st.markdown('**Comparación con la referencia histórica**')
   st.metric('Referencia histórica para la misma exposición (sin ajustes de condiciones)',f'{baseline*100:.2f} %',help='Probabilidad calculada usando únicamente la tasa anual histórica de accidentes y las horas-hombre de la cuadrilla.')
   diferencia=(p-baseline)*100
   if diferencia>0.01:
    st.warning(f'📈 **Variación frente a la referencia:** +{diferencia:.2f} puntos porcentuales. Las condiciones ingresadas elevan el pronóstico respecto de la frecuencia histórica de referencia.')
   elif diferencia < -0.01:
    st.success(f'📉 **Variación frente a la referencia:** {diferencia:.2f} puntos porcentuales. El escenario ingresado presenta un pronóstico inferior a la referencia.')
   else:
    st.info('➡️ El pronóstico coincide prácticamente con la referencia histórica.')
   if not controls or (iperc==3 and (acts or conds)):
    st.error('🔴 NO INICIAR: corregir controles críticos y reevaluar la actividad.')
   elif acts or conds or not epp or not preuso:
    st.warning('🟠 CORREGIR ANTES DE INICIAR: subsanar las desviaciones detectadas.')
   else:
    st.success('🟢 MANTENER CONTROLES: supervisión y verificación durante la actividad.')
   best_factor={1:.8,2:1.0,3:1.35}[iperc]
   best_p=1-np.exp(-tasa*hht*best_factor*(1.15 if avg_exp<2 else (1.05 if avg_exp<5 else 1.0)))
   best_inc=1-np.exp(-tasa_inc*hht*best_factor*(1.15 if avg_exp<2 else (1.05 if avg_exp<5 else 1.0)))
   st.markdown('#### ¿Qué está influyendo en el pronóstico?')
   factores=[('Nivel IPERC', {1:'Bajo',2:'Medio',3:'Alto'}[iperc],f_iperc),('Actos subestándares',str(len(acts)),f_act),('Condiciones subestándares',str(len(conds)),f_cond),('Estado de controles, EPP e inspección', 'Con desviaciones' if not (controls and epp and preuso) else 'Conformes',f_controls),('Experiencia media de la cuadrilla',f'{avg_exp:.1f} años',f_exp)]
   st.dataframe(pd.DataFrame(factores,columns=['Factor evaluado','Dato ingresado','Multiplicador de escenario']).style.format({'Multiplicador de escenario':'{:.2f} ×'}),hide_index=True,use_container_width=True)
   st.caption('Un multiplicador mayor que 1 incrementa la estimación respecto de la referencia; menor que 1 la reduce. Estos multiplicadores son parámetros preventivos definidos para el escenario, no coeficientes estadísticos aprendidos de los accidentes de la empresa.')
   st.markdown('#### Efecto esperado de corregir desviaciones')
   st.write(f'**Accidente incapacitante:** de **{p*100:.2f} %** a **{best_p*100:.2f} %** (cambio de **{(p-best_p)*100:.2f} puntos porcentuales**).')
   st.write(f'**Incidente:** de **{p_inc*100:.2f} %** a **{best_inc*100:.2f} %** (cambio de **{(p_inc-best_inc)*100:.2f} puntos porcentuales**).')
   st.caption('La comparación supone que se corrigen las desviaciones seleccionadas; no representa una reducción comprobada mediante intervención real.')
   comparison=pd.DataFrame({
    'Situación':['Condiciones ingresadas','Después de corregir desviaciones'],
    'Accidente incapacitante (%)':[100*p,100*best_p],
    'Incidente (%)':[100*p_inc,100*best_inc]})
   ca,cb=st.columns(2)
   with ca:
    st.plotly_chart(px.bar(comparison,x='Situación',y='Accidente incapacitante (%)',text_auto='.2f',title='Probabilidad mensual de accidente incapacitante',color_discrete_sequence=['#d35443']),use_container_width=True)
   with cb:
    st.plotly_chart(px.bar(comparison,x='Situación',y='Incidente (%)',text_auto='.2f',title='Probabilidad mensual de incidente · modelo de desarrollo',color_discrete_sequence=['#3276a8']),use_container_width=True)
   st.markdown('**Cómo leer los gráficos:** cada barra es la probabilidad de que ocurra **al menos un caso en toda la cuadrilla durante el mes seleccionado**. La primera barra usa las condiciones que ingresaste; la segunda muestra el resultado al corregir las desviaciones. Por ejemplo, 55 % no significa que 55 de cada 100 trabajadores tendrán un incidente, sino una probabilidad del 55 % de al menos un incidente en el grupo durante ese mes. Son escenarios de planificación, no certezas ni predicciones validadas.')
   resumen_resultado=pd.DataFrame({
    'Variable':['Año','Mes','Actividad','Trabajadores','HHT mensuales','Edad media','Experiencia media','IPERC','Actos subestándares','Condiciones subestándares','Prob. accidente incapacitante (%)','Prob. incidente · modelo de desarrollo (%)'],
    'Resultado':[year,MESES[month-1],actividad,n,round(hht,1),round(avg_age,1),round(avg_exp,1),{1:'Bajo',2:'Medio',3:'Alto'}[iperc],len(acts),len(conds),round(p*100,2),round(p_inc*100,2)]})
   st.download_button('⬇️ Descargar resultados del pronóstico (CSV)',resumen_resultado.to_csv(index=False).encode('utf-8-sig'),file_name=f'pronostico_{year}_{month:02d}.csv',mime='text/csv')
   st.markdown('**Medidas preventivas prioritarias**')
   measures=[]
   if acts: measures.append('Eliminar los actos subestándares detectados mediante supervisión, autorización y capacitación específica.')
   if conds: measures.append('Corregir y verificar el cierre de las condiciones subestándares antes de iniciar.')
   if not controls: measures.append('Implementar y verificar controles críticos obligatorios.')
   if not epp: measures.append('Comprobar EPP apropiado y su uso efectivo.')
   if not preuso: measures.append('Completar inspección preuso y retirar equipos no conformes.')
   if not measures: measures=['Mantener inspecciones, supervisión y controles existentes.']
   for m in measures: st.write('• '+m)
with t2:
 yearhist=st.selectbox('Seleccionar año',['Todos']+list(hist.anio.astype(int)),key='histyear')
 h=hist if yearhist=='Todos' else hist[hist.anio==yearhist]
 x,y,z=st.columns(3)
 x.metric('Accidentes incapacitantes',int(h.accidentes.sum()))
 y.metric('Días perdidos',int(h.dias_perdidos.sum()))
 z.metric('Horas hombre trabajadas',f'{int(h.hht.sum()):,}')
 st.dataframe(h.round(2).rename(columns=NOMBRES),hide_index=True,use_container_width=True)
 a,b=st.columns(2)
 with a: st.plotly_chart(px.bar(hist,x='anio',y='accidentes',labels={'anio':'Año','accidentes':'Accidentes incapacitantes'},text_auto=True,title='Accidentes incapacitantes por año'),use_container_width=True)
 with b: st.plotly_chart(px.bar(hist,x='anio',y='dias_perdidos',labels={'anio':'Año','dias_perdidos':'Días perdidos'},text_auto=True,title='Días perdidos por año'),use_container_width=True)
 st.markdown('### Indicadores de seguridad 2021–2025')
 st.caption('IF = accidentes incapacitantes × 1 000 000 / HHT · IS = días perdidos × 1 000 000 / HHT · IA = IF × IS / 1 000.')
 m1,m2,m3=st.columns(3)
 _if=h.accidentes.sum()*1_000_000/h.hht.sum()
 _is=h.dias_perdidos.sum()*1_000_000/h.hht.sum()
 m1.metric('IF del periodo seleccionado',f'{_if:.2f}')
 m2.metric('IS del periodo seleccionado',f'{_is:.2f}')
 m3.metric('IA del periodo seleccionado',f'{_if*_is/1000:.2f}')
 g1,g2=st.columns(2)
 with g1:
  fig_if=px.line(hist,x='anio',y='IF',markers=True,title='Índice de frecuencia (IF) por año')
  fig_if.update_traces(line=dict(width=3),marker=dict(size=9),text=hist['IF'].round(2),textposition='top center',mode='lines+markers+text')
  fig_if.update_layout(xaxis_title='Año',yaxis_title='Accidentes / millón de HHT')
  st.plotly_chart(fig_if,use_container_width=True)
 with g2:
  fig_is=px.line(hist,x='anio',y='IS',markers=True,title='Índice de severidad (IS) por año')
  fig_is.update_traces(line=dict(width=3),marker=dict(size=9),text=hist['IS'].round(2),textposition='top center',mode='lines+markers+text')
  fig_is.update_layout(xaxis_title='Año',yaxis_title='Días perdidos / millón de HHT')
  st.plotly_chart(fig_is,use_container_width=True)
 st.markdown('#### Índice de accidentabilidad (IA) por año')
 fig_ia=px.line(hist,x='anio',y='IA',markers=True,title='Índice de accidentabilidad = IF × IS / 1 000')
 fig_ia.update_traces(mode='lines+markers+text',text=hist['IA'].round(2),textposition='top center',line=dict(width=3),marker=dict(size=10))
 fig_ia.update_layout(xaxis_title='Año',yaxis_title='IA',height=340)
 st.plotly_chart(fig_ia,use_container_width=True)
 st.markdown('#### Tabla consolidada de los tres índices')
 st.dataframe(hist[['anio','accidentes','dias_perdidos','hht','IF','IS','IA']].round(2).rename(columns=NOMBRES),hide_index=True,use_container_width=True)
with t3:
 st.subheader('Consulta de antecedentes mensuales y registros de análisis')
 st.markdown('### Calendario mensual de accidentes e incidentes · 2021–2025')
 mensual_hist=tabla_mensual()
 c1,c2=st.columns(2)
 with c1: a_f=st.selectbox('Filtrar año',['Todos']+list(range(2021,2026)),key='mes_anio')
 with c2: m_f=st.selectbox('Filtrar mes',['Todos']+MESES,key='mes_nombre')
 vista=mensual_hist.copy()
 if a_f!='Todos': vista=vista[vista['Año']==a_f]
 if m_f!='Todos': vista=vista[vista['Mes']==m_f]
 st.dataframe(vista[['Año','Mes','Accidentes incapacitantes','Accidentes no incapacitantes','Incidentes']],hide_index=True,use_container_width=True,height=310)
 st.download_button('Descargar tabla de antecedentes mensuales',vista.to_csv(index=False).encode('utf-8-sig'),file_name='antecedentes_mensuales.csv',mime='text/csv')
 st.markdown('### Registro de accidentes · control interno')
 st.dataframe(reg_acc.assign(procedencia='Registros internos').rename(columns={'anio':'Año','mes':'Mes','fecha':'Fecha','actividad':'Actividad','clasificacion':'Clasificación','descripcion':'Descripción','procedencia':'Origen del registro'}),hide_index=True,use_container_width=True)
 st.markdown('### Registro detallado de incidentes 2021–2025')
 incidentes=reg_inc.copy()
 ca,cb=st.columns(2)
 with ca: ai=st.selectbox('Año de incidentes',['Todos']+list(range(2021,2026)),key='inc_year')
 with cb: mi=st.selectbox('Mes de incidentes',['Todos']+list(range(1,13)),key='inc_month',format_func=lambda x: MESES[x-1] if isinstance(x,int) else x)
 filtrado=incidentes.copy()
 if ai!='Todos': filtrado=filtrado[filtrado.anio==ai]
 if mi!='Todos': filtrado=filtrado[filtrado.mes==mi]
 st.metric('Incidentes en el calendario de evaluación',len(filtrado))
 st.dataframe(filtrado.rename(columns=NOMBRES),hide_index=True,use_container_width=True,height=260)
 resumen=incidentes.groupby(['anio','mes'],as_index=False).size().rename(columns={'size':'incidentes'})
 resumen['Mes']=resumen.mes.map(lambda x: MESES[x-1])
 resumen['Año']=resumen.anio.astype(str)
 fig_inc=px.bar(resumen,x='Mes',y='incidentes',color='Año',barmode='group',title='Distribución mensual de incidentes · escenario de evaluación',labels={'incidentes':'Número de incidentes'})
 fig_inc.update_xaxes(categoryorder='array',categoryarray=MESES)
 st.plotly_chart(fig_inc,use_container_width=True)
 st.download_button('Descargar registro de incidentes (CSV)',incidentes.to_csv(index=False).encode('utf-8-sig'),file_name='registro_incidentes.csv')

 st.markdown('**Registros de análisis del modelo (no equivalen a accidentes históricos)**')
 a,b=st.columns(2)
 with a: yy=st.selectbox('Año',['Todos']+list(range(2021,2026)),key='data_year')
 with b: mm=st.selectbox('Mes',['Todos']+list(range(1,13)),format_func=lambda x:MESES[x-1] if isinstance(x,int) else x,key='data_month')
 sub=data.copy()
 if yy!='Todos': sub=sub[sub.anio==yy]
 if mm!='Todos': sub=sub[sub.mes==mm]
 st.metric('Registros de análisis filtrados',len(sub))
 st.dataframe(sub.rename(columns=NOMBRES).replace({'Temporada':{0:'Temporada habitual',1:'Temporada de mayor exposición'}}),hide_index=True,use_container_width=True,height=340)
 st.download_button('Descargar registros filtrados (CSV)',sub.to_csv(index=False).encode(),file_name='registros_analisis.csv')
 st.caption('La tabla de registros complementarios se utiliza para el desarrollo y prueba del modelo. Los valores por mes no son el registro histórico verificado de accidentes incapacitantes.')
 monthly=sub.groupby('mes',as_index=False).agg(actos=('acto_subestandar','sum'),condiciones=('condicion_subestandar','sum'))
 st.plotly_chart(px.bar(monthly.rename(columns={'mes':'Mes','actos':'Actos subestándares','condiciones':'Condiciones subestándares'}),x='Mes',y=['Actos subestándares','Condiciones subestándares'],barmode='group',title='Actos y condiciones subestándares por mes — registros de análisis'),use_container_width=True)
 st.info('Los accidentes incapacitantes históricos están disponibles por año, no por mes. No se atribuyen meses específicos a esos accidentes sin documentos de respaldo.')
with t4:
 st.markdown("""### Alcance estadístico
**Histórico anual 2021–2025:** se utiliza para establecer la frecuencia base de accidentes incapacitantes por hora hombre trabajada.

**Pronóstico mensual:** se calcula la exposición esperada de la cuadrilla y la probabilidad de al menos un accidente incapacitante con un modelo de conteo de Poisson, ajustado por condiciones de seguridad. Los factores de ajuste son parámetros de escenario y no coeficientes aprendidos de los siete accidentes históricos.

**Regresión logística:** los modelos exploratorios de accidentes e incidentes están incluidos en el paquete para investigación, pero fueron entrenados con registros generados para la demostración. No constituyen una validación predictiva con datos empresariales reales.

**Incidentes:** se incorpora un registro separado de 50 incidentes de práctica (2021–2025), con fechas, actividades, causas y medidas. Estos registros NO son reportes verificados de la empresa; la probabilidad correspondiente es ilustrativa.

**Carga de antecedentes mensuales:** el archivo `registro_mensual.csv` admite el número de accidentes incapacitantes, accidentes no incapacitantes e incidentes por cada mes de 2021–2025. Dejar vacío significa información no disponible, no cero. Para incorporar nuevos registros, actualizar ese CSV y reiniciar la aplicación.\n\n**Alcance de los registros:** los totales anuales corresponden a la información proporcionada; la distribución mensual y los incidentes añadidos para evaluar el sistema no están respaldados por partes originales.\n\n**Interpretación de los resultados:** los totales anuales y el calendario mensual de evaluación tienen alcances distintos. El pronóstico orienta la prevención y no certifica que un accidente vaya a ocurrir en una fecha determinada.

**Edad:** se utiliza para caracterizar la cuadrilla, no para discriminar ni para atribuir causalidad por sí sola. La experiencia modifica el escenario preventivo mediante un parámetro explícito.
""")
 st.markdown('#### Diccionario de actos subestándares')
 st.dataframe(pd.DataFrame({'Acto subestándar':ACTOS}),hide_index=True,use_container_width=True)
 st.markdown('#### Diccionario de condiciones subestándares')
 st.dataframe(pd.DataFrame({'Condición subestándar':COND}),hide_index=True,use_container_width=True)
