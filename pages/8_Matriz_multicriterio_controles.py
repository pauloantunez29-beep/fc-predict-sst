import streamlit as st
import pandas as pd
from pathlib import Path
st.set_page_config(page_title="Matriz multicriterio SST", layout="wide")
st.title("Matriz multicriterio de medidas de control")
st.caption("FC PREDICT SST 7.1 · módulo de decisiones preventivas por escenario")
st.caption("Puntuaciones de referencia editables. El modelo Poisson estima conteos globales por cuadrilla-mes, no probabilidades por mecanismo de lesión.")
st.markdown("**Unidad de evaluación:** actividad + peligro + riesgo o daño potencial. Compare medidas alternativas para un mismo escenario, no puntajes de riesgos diferentes.")
df=pd.read_csv(Path(__file__).resolve().parent.parent/'matriz_multicriterio_ejemplo.csv')
HAZARDS={
 'Esmerilado / corte':('Disco abrasivo en rotación, aristas y partículas proyectadas','Contacto con disco, cortes y lesiones oculares'),
 'Soldadura':('Humos metálicos generados durante la soldadura','Inhalación de contaminantes y posibles daños respiratorios'),
 'Montaje y manipulación':('Perfiles pesados, bordes cortantes y cargas en movimiento','Golpes, aplastamiento y lesiones musculoesqueléticas'),
 'Trabajo con estructuras':('Piezas inestables y estructuras susceptibles de vuelco','Golpes o aplastamiento por caída o vuelco de piezas'),
}
scenarios=df[['actividad','riesgo']].drop_duplicates()
labels=[f"{x.actividad} — {x.riesgo}" for x in scenarios.itertuples(index=False)]
choice=st.selectbox('Escenario de riesgo',labels)
idx=labels.index(choice);a=scenarios.iloc[idx]['actividad'];r=scenarios.iloc[idx]['riesgo']
subset=df[(df.actividad==a)&(df.riesgo==r)].copy()
hazard,damage=HAZARDS.get(a,('Peligro por identificar mediante IPERC',r))
st.markdown('### Identificación del escenario')
st.dataframe(pd.DataFrame([{'Actividad':a,'Peligro (fuente o situación)':hazard,'Riesgo o daño potencial':damage}]),hide_index=True,use_container_width=True)
st.caption('La descripción del peligro se utiliza para seleccionar controles; el riesgo describe el evento y sus posibles consecuencias.')
st.markdown('### Ponderaciones de referencia del docente')
weights={'eficacia':.45,'viabilidad':.20,'costo':.15,'tiempo':.10,'impacto_produccion':.10}
st.dataframe(pd.DataFrame([{'Criterio':k.replace('_',' ').capitalize(),'Peso':f'{v:.0%}'} for k,v in weights.items()]),hide_index=True,use_container_width=True)
st.info('Calificaciones de referencia para una metalmecánica pequeña: juicio técnico preliminar, editable según inspección, cotizaciones y condiciones de la tarea. No representan mediciones verificadas.')
with st.expander('Escala 1 a 5: criterios de asignación', expanded=True):
 st.dataframe(pd.DataFrame([
 {'Valor':1,'Eficacia':'Muy baja','Viabilidad':'Muy difícil','Costo':'Muy alto','Tiempo':'Muy largo','Producción':'Impacto muy alto'},
 {'Valor':2,'Eficacia':'Baja','Viabilidad':'Difícil','Costo':'Alto','Tiempo':'Largo','Producción':'Impacto alto'},
 {'Valor':3,'Eficacia':'Media','Viabilidad':'Moderada','Costo':'Medio','Tiempo':'Medio','Producción':'Impacto medio'},
 {'Valor':4,'Eficacia':'Alta','Viabilidad':'Fácil','Costo':'Bajo','Tiempo':'Corto','Producción':'Impacto bajo'},
 {'Valor':5,'Eficacia':'Muy alta','Viabilidad':'Muy fácil','Costo':'Muy bajo','Tiempo':'Muy corto','Producción':'Impacto mínimo'}
 ]),hide_index=True,use_container_width=True)
 st.caption('Costo, tiempo y producción se puntúan por conveniencia: 5 = mejor. El valor 5 en eficacia debe sustentarse en eliminación efectiva del peligro o reducción demostrable de la exposición.')
cols=['codigo','medida','jerarquia']+list(weights)
for k in weights:subset[k]=subset[k].astype(int)
config={k:st.column_config.NumberColumn(k.replace('_',' ').capitalize(),min_value=1,max_value=5,step=1,required=True) for k in weights}
edit=st.data_editor(subset[cols],hide_index=True,use_container_width=True,num_rows='fixed',disabled=['codigo','medida','jerarquia'],column_config=config,key=f'edit_{idx}')
for k in weights:edit[k]=pd.to_numeric(edit[k],errors='coerce').fillna(1).clip(1,5)
edit['puntaje']=sum(edit[k]*w for k,w in weights.items())
rank=edit.sort_values('puntaje',ascending=False)
st.markdown('### Jerarquía completa de controles')
st.markdown('**1. Eliminación → 2. Sustitución → 3. Ingeniería → 4. Administrativos → 5. EPP.** Todas las alternativas se muestran y evalúan. Las dos últimas son medidas complementarias: no sustituyen una opción superior viable que controle eficazmente el peligro.')
st.markdown('### Resultado: ranking de alternativas')
rank['orden']=rank['puntaje'].rank(method='min',ascending=False).astype(int)
st.caption('Las puntuaciones de 1 a 5 son valoraciones técnicas iniciales. La decisión definitiva exige comprobar la eficacia y factibilidad de cada medida.')
st.dataframe(rank[['orden','codigo','medida','jerarquia','eficacia','viabilidad','costo','tiempo','impacto_produccion','puntaje']],hide_index=True,use_container_width=True)
for nivel in ['Eliminación','Sustitución','Ingeniería','Administrativo','EPP']:
 grupo=rank[rank['jerarquia'].str.casefold()==nivel.casefold()]
 if not grupo.empty:
  st.markdown(f'**{nivel}:** ' + '; '.join(grupo['medida'].astype(str).tolist()))
st.bar_chart(rank.set_index('codigo')['puntaje'])
best=rank.iloc[0]
st.info(f"Mayor puntaje económico-operativo global: {best['codigo']} — {best['medida']} ({best['puntaje']:.2f}/5). No constituye una autorización de uso ni sustituye la jerarquía.")
upper=rank[rank['jerarquia'].isin(['Eliminación','Sustitución','Ingeniería'])].sort_values('puntaje',ascending=False)
if not upper.empty:
 top=upper.iloc[0]
 st.success(f"Alternativa superior a evaluar prioritariamente: {top['codigo']} — {top['medida']} ({top['jerarquia']}; {top['puntaje']:.2f}/5). Verificar su capacidad real de controlar el peligro y factibilidad antes de decidir.")
st.error('Regla crítica: ante ausencia de un control esencial y riesgo grave o inminente, detener la exposición y corregir antes de reanudar. El ranking no autoriza aceptar el riesgo.')
st.markdown('### Decisión y verificación')
st.write('Priorizar eliminación, sustitución e ingeniería cuando sean viables y eficaces. Mantener procedimientos, permisos, inspecciones, supervisión y EPP como barreras complementarias. Documentar la razón técnica de no elegir una alternativa superior y verificar la eficacia del conjunto de controles.')
st.markdown('### Plan de implementación de la alternativa seleccionada')
selection=st.selectbox('Medida que se evaluará para implementación',rank['codigo'].tolist(),index=0)
selected=rank.loc[rank['codigo']==selection].iloc[0]
st.write(f"**Medida:** {selected['medida']} · **Jerarquía:** {selected['jerarquia']}")
c1,c2=st.columns(2)
with c1:
 responsable=st.text_input('Responsable','Responsable SST / jefe de taller')
 presupuesto=st.text_input('Presupuesto referencial (S/)','Por cotizar')
with c2:
 plazo=st.text_input('Plazo previsto','Por definir')
 indicador=st.text_input('Indicador de eficacia','% de puestos con control implementado y verificado')
verificacion=st.text_area('Verificación técnica / evidencia requerida','Inspección del puesto, comprobación del control y actualización del IPERC')
plan=pd.DataFrame([{'actividad':a,'peligro':hazard,'riesgo_o_dano_potencial':damage,'codigo':selection,'medida':selected['medida'],'jerarquia':selected['jerarquia'],'puntaje':selected['puntaje'],'responsable':responsable,'presupuesto':presupuesto,'plazo':plazo,'indicador':indicador,'verificacion':verificacion}])
st.download_button('Descargar plan de implementación CSV',plan.to_csv(index=False).encode('utf-8-sig'),file_name='plan_control_preventivo.csv',mime='text/csv')
export=rank.copy()
export.insert(0,'actividad',a)
export.insert(1,'peligro',hazard)
export.insert(2,'riesgo_o_dano_potencial',damage)
st.download_button('Descargar evaluación CSV',export.to_csv(index=False).encode('utf-8-sig'),file_name='evaluacion_multicriterio.csv',mime='text/csv')
