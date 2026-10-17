import streamlit as st
import pandas as pd
st.set_page_config(page_title="Priorización preventiva",layout="wide")
st.title("Priorización preventiva: actividad, peligro y riesgo")
st.caption("FC PREDICT SST 7.1 · Tabla de revisión preventiva y condiciones críticas")
data=[
("Soldadura","Partes energizadas, conductores deteriorados y materiales combustibles","Contacto eléctrico, quemaduras o incendio","Inmediata si falta un control crítico","Detener o no iniciar; aislar fuentes de ignición, revisar instalación eléctrica y restituir barreras críticas"),
("Montaje en altura","Bordes sin protección y superficies elevadas","Caída a distinto nivel","Inmediata si existe exposición sin protección","Evitar trabajo en altura mediante preensamble a nivel de suelo; instalar protección colectiva y verificar accesos"),
("Corte y esmerilado","Disco en rotación y partículas proyectadas","Contacto con disco, cortes o lesión ocular","Alta; inmediata ante guarda ausente o disco defectuoso","Eliminar cortes innecesarios; emplear sujeción y guardas compatibles; retirar equipos defectuosos"),
("Soldadura","Humos metálicos, radiación óptica y partículas calientes","Inhalación de humos, daño ocular o quemaduras","Alta según exposición","Sustituir proceso cuando sea viable; instalar extracción localizada y pantallas; complementar con controles administrativos y EPP"),
("Manipulación de perfiles","Perfiles pesados y movimientos manuales repetidos","Sobreesfuerzo, golpes o aplastamiento","Programada; inmediata si hay inestabilidad grave","Eliminar traslados innecesarios; utilizar mesas elevadoras, rodillos y apoyos estables")]
df=pd.DataFrame(data,columns=['Actividad','Peligro','Riesgo o daño potencial','Prioridad de revisión','Decisión preventiva propuesta'])
st.dataframe(df,hide_index=True,use_container_width=True)
st.error("Si falta una barrera crítica ante peligro grave o inminente, detener la exposición. La prioridad no depende del puntaje multicriterio.")
st.markdown("**Secuencia:** identificar actividad → peligro → riesgo → condición crítica → comparar controles en la matriz multicriterio → planificar y verificar.")
st.download_button("Descargar tabla preventiva CSV",df.to_csv(index=False).encode('utf-8-sig'),file_name='prioridades_preventivas.csv',mime='text/csv')
