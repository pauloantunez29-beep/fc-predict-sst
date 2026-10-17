import streamlit as st
import pandas as pd
from datetime import date
from io import StringIO

st.set_page_config(page_title="Evaluación SST por actividad", page_icon="🛡️", layout="wide")
st.title("🛡️ Evaluación SST por actividad")
st.write("Selecciona una tarea del taller o registra una nueva. El sistema separa el peligro, el riesgo y las medidas de control para apoyar una decisión preventiva.")

CASES = {
 "Corte y esmerilado": {
  "peligro":"Disco abrasivo en rotación; piezas sin sujeción; proyección de fragmentos",
  "riesgo":"Contacto con el disco o impacto de partículas proyectadas",
  "consecuencia":"Cortes profundos y lesiones oculares",
  "criticos":["Guarda compatible y correctamente instalada", "Disco íntegro y compatible con velocidad del equipo", "Pieza sujeta de forma estable"],
  "medidas":[("Eliminación","Adquirir perfiles precortados y desbarbados, eliminando el corte interno cuando sea factible"),("Sustitución","Usar un proceso de corte alternativo de menor exposición, tras evaluación técnica"),("Ingeniería","Instalar resguardos compatibles, pantallas de contención y mordazas de sujeción"),("Administrativo","Inspección preuso, procedimiento de trabajo y retiro de discos defectuosos"),("EPP","Protección ocular y facial compatible con la tarea")]
 },
 "Soldadura": {
  "peligro":"Arco eléctrico, conductores energizados, humos y material combustible cercano",
  "riesgo":"Contacto eléctrico, inhalación de humos, radiación y proyección de chispas",
  "consecuencia":"Electrocución, quemaduras, lesión ocular y afección respiratoria",
  "criticos":["Equipo eléctrico y cables en buen estado", "Material combustible retirado o protegido", "Ventilación o extracción apropiada a la exposición"],
  "medidas":[("Eliminación","Utilizar uniones mecánicas o componentes prefabricados cuando el diseño lo permita"),("Sustitución","Evaluar consumibles o proceso con menor emisión de humos"),("Ingeniería","Instalar extracción localizada, pantallas y protecciones eléctricas"),("Administrativo","Permiso de trabajo en caliente, inspección y vigilancia de incendios según evaluación"),("EPP","Careta para soldar, protección de manos y respiratoria según exposición")]
 },
 "Montaje en altura": {
  "peligro":"Bordes abiertos, plataformas elevadas y accesos inestables",
  "riesgo":"Caída a distinto nivel",
  "consecuencia":"Lesiones graves o muerte",
  "criticos":["Acceso y plataforma estables", "Protección colectiva o sistema anticaídas definido", "Puntos de anclaje verificados cuando correspondan"],
  "medidas":[("Eliminación","Preensamblar componentes a nivel de suelo"),("Sustitución","Emplear método de montaje que reduzca la necesidad de acceder a altura"),("Ingeniería","Plataformas adecuadas y barandas o protección colectiva"),("Administrativo","Permiso de trabajo, inspección y plan de rescate"),("EPP","Sistema personal anticaídas cuando corresponda")]
 },
 "Manipulación de perfiles": {
  "peligro":"Perfiles pesados, aristas cortantes y cargas inestables",
  "riesgo":"Atrapamiento, golpe, corte o sobreesfuerzo",
  "consecuencia":"Lesión musculoesquelética, contusión o aplastamiento",
  "criticos":["Carga estable y recorrido despejado", "Medio de izaje o transporte apropiado a la carga", "Accesorios inspeccionados cuando se utilicen"],
  "medidas":[("Eliminación","Eliminar traslados mediante reorganización del flujo y entrega en punto de uso"),("Sustitución","Utilizar perfiles de menor peso cuando el diseño lo permita"),("Ingeniería","Mesas elevadoras, rodillos y dispositivos de sujeción"),("Administrativo","Planificación de maniobras y delimitación de zonas"),("EPP","Guantes y calzado de seguridad adecuados")]
 },
 "Uso de taladro": {
  "peligro":"Broca giratoria, pieza sin fijación y puntos de atrapamiento",
  "riesgo":"Atrapamiento o contacto con partes giratorias",
  "consecuencia":"Cortes, fracturas o lesión en manos",
  "criticos":["Pieza fijada con mordaza", "Protección de transmisión y componentes en buen estado", "Parada y desconexión seguras"],
  "medidas":[("Eliminación","Adquirir piezas perforadas de origen cuando resulte viable"),("Sustitución","Usar proceso alternativo que evite perforación manual, sujeto a evaluación"),("Ingeniería","Mordazas, resguardos y dispositivos de parada"),("Administrativo","Procedimiento, inspección y prohibición de prendas sueltas"),("EPP","Protección ocular; evitar guantes cerca de elementos giratorios expuestos")]
 }
}

selection=st.selectbox("Actividad a evaluar",list(CASES)+["Otra actividad (registrar)"])
custom=selection.startswith('Otra')
if custom:
 actividad=st.text_input('Nombre de la actividad',placeholder='Ej.: uso de tronzadora')
 record={'peligro':'','riesgo':'','consecuencia':'','criticos':[], 'medidas':[]}
else:
 actividad=selection
 record=CASES[selection]

st.subheader('1. Identificar peligro y riesgo')
col1,col2=st.columns(2)
with col1:
 peligro=st.text_area('Peligro: fuente o situación capaz de causar daño',value=record['peligro'],height=110,key=f'p_{selection}')
 riesgo=st.text_area('Riesgo: evento peligroso que puede ocurrir',value=record['riesgo'],height=90,key=f'r_{selection}')
with col2:
 consecuencia=st.text_area('Consecuencia posible',value=record['consecuencia'],height=90,key=f'c_{selection}')
 lugar=st.text_input('Área o frente de trabajo',value='Taller metalmecánico')

st.subheader('2. Comprobar controles críticos')
st.caption('Marca solo los controles que verificaste en campo. No equivale a una inspección real hasta registrar evidencia.')
criticos=record['criticos'] if record['criticos'] else ['Equipo y accesorios en condiciones seguras','Protecciones colectivas o barreras críticas verificadas','Condiciones de operación seguras']
with st.container(border=True):
 respuestas=[]
 for i,item in enumerate(criticos):
  respuestas.append(st.checkbox(item,key=f'{selection}_{i}'))
 condicion=st.radio('¿Se observa una condición de peligro grave o inminente?', ['No se ha identificado','Sí','Aún no se ha inspeccionado'],horizontal=True)
 faltantes=[x for x,ok in zip(criticos,respuestas) if not ok]
 if condicion=='Sí':
  prioridad='INMEDIATA — DETENER / NO INICIAR'
  st.error('No iniciar o interrumpir la actividad afectada. Corregir la condición crítica y verificar antes de reanudar.')
 elif faltantes or condicion=='Aún no se ha inspeccionado':
  prioridad='VERIFICACIÓN PENDIENTE — NO AUTORIZA INICIO'
  st.warning('Faltan controles críticos por verificar. No considerar esta evaluación como autorización para trabajar.')
 else:
  prioridad='REVISIÓN PREVENTIVA PROGRAMADA'
  st.success('Los controles indicados fueron marcados como verificados. Confirmar evidencia, IPERC y condiciones reales antes de autorizar.')

st.subheader('3. Seleccionar medidas según jerarquía')
st.write('Se muestran alternativas en orden de preferencia preventiva. La viabilidad y eficacia deben comprobarse; una puntuación económica no sustituye la jerarquía.')
jer=['Eliminación','Sustitución','Ingeniería','Administrativo','EPP']
base={j:t for j,t in record['medidas']}
medidas=[]
for j in jer:
 texto=st.text_area(j, value=base.get(j,''),height=75,key=f'm_{selection}_{j}',placeholder='Escribe una medida específica para esta actividad')
 if texto.strip(): medidas.append((j,texto.strip()))
choice=st.selectbox('Medida principal propuesta', [f'{j}: {t}' for j,t in medidas] if medidas else ['Pendiente de definir'])
justificacion=st.text_area('Justificación técnica de la medida elegida',placeholder='Explica qué peligro elimina o cómo evita/reduce la exposición; por qué es viable en esta tarea.')

st.subheader('4. Plan de acción y verificación')
a,b=st.columns(2)
with a:
 responsable=st.text_input('Responsable de implementar',placeholder='Ej.: jefe de taller')
 plazo=st.date_input('Fecha objetivo',value=date.today())
with b:
 evidencia=st.text_input('Evidencia requerida',placeholder='Ej.: inspección, fotografía, prueba funcional, IPERC actualizado')
 indicador=st.text_input('Cómo se comprobará la eficacia',placeholder='Ej.: operación sin exposición al disco en tareas verificadas')
observaciones=st.text_area('Observaciones de la inspección',placeholder='Registra hallazgos reales. Si es una demostración, indícalo.')

st.subheader('5. Resultado para revisión SST')
st.markdown(f'**Actividad:** {actividad or "Sin especificar"}  \n**Peligro:** {peligro or "Pendiente"}  \n**Riesgo:** {riesgo or "Pendiente"}  \n**Prioridad:** {prioridad}  \n**Medida principal:** {choice}')
if not justificacion.strip(): st.info('Falta justificar técnicamente la alternativa seleccionada antes de aprobar la intervención.')
if not evidencia.strip() or not indicador.strip(): st.info('Completa la evidencia y el indicador para verificar si el control realmente funciona.')

registro={'Fecha de evaluación':str(date.today()),'Actividad':actividad,'Área':lugar,'Peligro':peligro,'Riesgo':riesgo,'Consecuencia':consecuencia,'Prioridad':prioridad,'Controles críticos sin verificar':' | '.join(faltantes),'Condición grave o inminente':condicion,'Medida principal':choice,'Justificación técnica':justificacion,'Responsable':responsable,'Fecha objetivo':str(plazo),'Evidencia':evidencia,'Indicador':indicador,'Observaciones':observaciones}
for j,t in medidas: registro['Control '+j]=t
st.download_button('📥 Descargar ficha de evaluación SST (CSV)',pd.DataFrame([registro]).to_csv(index=False).encode('utf-8-sig'),file_name='evaluacion_SST_actividad.csv',mime='text/csv',use_container_width=True)
st.caption('Herramienta de apoyo. Los ejemplos no acreditan controles instalados ni datos reales de FC Estructuras. La autorización del trabajo exige verificación presencial, IPERC y procedimientos aplicables.')
