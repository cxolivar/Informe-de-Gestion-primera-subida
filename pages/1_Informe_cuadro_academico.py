import streamlit as st
import pyodbc
import pandas as pd
import time
import numpy as np
import seaborn as sns



#################### EXTRACCION DE LA BASE DE DATOS DESDE 2022 EN ADELANTE ###############################


# server = 'svr-uautonoma-prd.database.windows.net'
# database = 'db-uautonoma-prd'
# username = 'sa_uautonoma'
# password = 'Admin.prd.2023!'
# driver = 'ODBC Driver 18 for SQL Server' 



# # Establecer la conexión
# conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')

### llamo a la tabla de los estandar de secciones.
estandar=pd.read_excel("G:/Mi unidad/Camilo Olivares/Finanzas/Python/Informe de Gestion estático/pages/Datos_estandar.xlsx")
tabla_final_antiguo=pd.read_excel("G:/Mi unidad/Camilo Olivares/Finanzas/Python/Informe de Gestion estático/pages/tabla_final_antiguo_no_borrar.xlsx")


# # Función para ejecutar consultas y devolver un DataFrame
# @st.cache_data
# def ejecutar_consulta(query):
#     return pd.read_sql(query, conn)

# #consulta a la base de datos
# df_base = ejecutar_consulta("SELECT * FROM STG.UWVPRES WHERE UWVPRES_TERM_CODE > 202153")
# df_base_inscritos = ejecutar_consulta("SELECT * FROM STG.UWVPLNI")

# df_base.to_csv("df_base.csv")
df_base=pd.read_csv("G:/Mi unidad/Camilo Olivares/Finanzas/Python/Informe de Gestion estático/pages/df_base.csv")
# df_base_inscritos.to_csv("df_base_inscritos.csv")
df_base_inscritos=pd.read_csv("G:/Mi unidad/Camilo Olivares/Finanzas/Python/Informe de Gestion estático/pages/df_base_inscritos.csv")

df_base_inscritos["LLAVE"]=df_base_inscritos["UWVPLNI_TERM_CODE"]+df_base_inscritos["UWVPLNI_CRN"]


df_principal=df_base[["UWVPRES_TERM_CODE","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_AREA_PRIORITY","UWVPRES_CRN","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_CAMPUS","UWVPRES_TIPO_CURSO"]]
df_principal["INSCRITOS"]=0
df_principal["LLAVE"]=df_principal["UWVPRES_TERM_CODE"]+df_principal["UWVPRES_CRN"]

# acá se colocan el numero de inscritos y es la base que mantienen todos los nrc
df_principal=pd.merge(df_principal,df_base_inscritos,on="LLAVE")
df_principal=df_principal[["UWVPRES_TERM_CODE","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_AREA_PRIORITY","UWVPRES_CRN","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_CAMPUS","UWVPRES_TIPO_CURSO","UWVPLNI_INSCRITOS"]]
df_principal=df_principal.drop_duplicates(keep="first")

#df_principal.to_excel("df_principal.xlsx")


# acá se hace la suma de inscritos y total secciones
total_inscritos=pd.pivot_table(df_principal,
                                      values="UWVPLNI_INSCRITOS",
                                      index=["UWVPRES_TERM_CODE","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_AREA_PRIORITY","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_CAMPUS","UWVPRES_TIPO_CURSO"], 
                                      aggfunc="sum")
total_inscritos=total_inscritos.reset_index()  #devuelte la tabla dinamica a un dataframe normal


total_sesiones=pd.pivot_table(df_principal,
                                      values="UWVPLNI_INSCRITOS",
                                      index=["UWVPRES_TERM_CODE","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_AREA_PRIORITY","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_CAMPUS","UWVPRES_TIPO_CURSO"], 
                                      aggfunc="count")
total_sesiones=total_sesiones.reset_index() #devuelte la tabla dinamica a un dataframe normal

tabla_intermedia=pd.merge(total_inscritos,total_sesiones,on=["UWVPRES_TERM_CODE","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_AREA_PRIORITY","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_CAMPUS","UWVPRES_TIPO_CURSO"])


#CAMBIO DE LOS NOMBRE DE COLUMNAS
tabla_intermedia=tabla_intermedia.rename(columns={"UWVPRES_TERM_CODE":"PERIODO",
                                        "UWVPRES_PROGRAMA":"CODIGO_PROGRAMA",
                                        "UWVPRES_NOMBRE_PROGRAMA":"PROGRAMA",
                                        "UWVPRES_AREA_PRIORITY":"NIVEL",
                                        "UWVPRES_SUBJ_CODE":"MATERIA",
                                        "UWVPRES_CRSE_NUMB":"CURSO",
                                        "UWVPRES_NOMBRE_CURSO":"TITULO",
                                        "UWVPRES_CAMPUS":"SEDE",
                                        "UWVPRES_TIPO_CURSO":"TIPO_HORARIO",
                                        "UWVPLNI_INSCRITOS_x":"TOTAL_INSCRITOS",
                                        "UWVPLNI_INSCRITOS_y":"TOTAL_SECCIONES"})



tabla_final=pd.merge(tabla_intermedia, estandar,on=["CODIGO_PROGRAMA","PROGRAMA","MATERIA","CURSO","TITULO","TIPO_HORARIO"],how="left")
tabla_final=tabla_final.drop_duplicates()

#tabla_final.to_excel("tabla_final.xlsx")

tabla_final["SECCIONES_ESTANDAR"]=np.ceil(tabla_final["TOTAL_INSCRITOS"]/tabla_final["Estandar"])


##############################


#########################################TABLA CORPORTATIVO############
periodos=[202210,202220,202310,202320,202410,202420]
tabla_total=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final[tabla_final["PERIODO"]==periodo]
    
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total=pd.merge(tabla_total, aux,on="TIPO_HORARIO",how="left")


periodos=[201610,201620,201710,201720,201810,201820,201910,201920,202010,202020,202110,202120]
tabla_total_2016=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final_antiguo[tabla_final_antiguo["PERIODO"]==periodo]
    
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_2016=pd.merge(tabla_total_2016, aux,on="TIPO_HORARIO",how="left")


tabla_corporativa_historica=tabla_total_2016.merge(tabla_total,on="TIPO_HORARIO")





#########################################TABLA SEDES: PROVIDENCIA ############
periodos=[202210,202220,202310,202320,202410,202420]
sedes="Providencia"


tabla_total_providencia=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final[tabla_final["PERIODO"]==periodo]
    tabla_auxiliar=tabla_auxiliar[tabla_auxiliar["SEDE"]==sedes]
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_providencia=pd.merge(tabla_total_providencia, aux,on="TIPO_HORARIO",how="left")


periodos=[201610,201620,201710,201720,201810,201820,201910,201920,202010,202020,202110,202120]
tabla_total_2016=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final_antiguo[tabla_final_antiguo["PERIODO"]==periodo]
    tabla_auxiliar=tabla_auxiliar[tabla_auxiliar["SEDE"]==sedes]    
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_2016=pd.merge(tabla_total_2016, aux,on="TIPO_HORARIO",how="left")




tabla_historica_providencia=tabla_total_2016.merge(tabla_total_providencia,on="TIPO_HORARIO")















#########################################TABLA SEDES: SAN MIGUEL ############
periodos=[202210,202220,202310,202320,202410,202420]
sedes="San Miguel"


tabla_total_sanmiguel=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final[tabla_final["PERIODO"]==periodo]
    tabla_auxiliar=tabla_auxiliar[tabla_auxiliar["SEDE"]==sedes]
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_sanmiguel=pd.merge(tabla_total_sanmiguel, aux,on="TIPO_HORARIO",how="left")
    
    
    
periodos=[201610,201620,201710,201720,201810,201820,201910,201920,202010,202020,202110,202120]
tabla_total_2016=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final_antiguo[tabla_final_antiguo["PERIODO"]==periodo]
    tabla_auxiliar=tabla_auxiliar[tabla_auxiliar["SEDE"]==sedes]    
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_2016=pd.merge(tabla_total_2016, aux,on="TIPO_HORARIO",how="left")




tabla_historica_sanmiguel=tabla_total_2016.merge(tabla_total_sanmiguel,on="TIPO_HORARIO")
    
    
    

#########################################TABLA SEDES: TALCA ############
periodos=[202210,202220,202310,202320,202410,202420]
sedes="Talca"


tabla_total_talca=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final[tabla_final["PERIODO"]==periodo]
    tabla_auxiliar=tabla_auxiliar[tabla_auxiliar["SEDE"]==sedes]
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_talca=pd.merge(tabla_total_talca, aux,on="TIPO_HORARIO",how="left")
    
    
periodos=[201610,201620,201710,201720,201810,201820,201910,201920,202010,202020,202110,202120]
tabla_total_2016=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final_antiguo[tabla_final_antiguo["PERIODO"]==periodo]
    tabla_auxiliar=tabla_auxiliar[tabla_auxiliar["SEDE"]==sedes]    
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_2016=pd.merge(tabla_total_2016, aux,on="TIPO_HORARIO",how="left")




tabla_historica_talca=tabla_total_2016.merge(tabla_total_talca,on="TIPO_HORARIO")
    

#########################################TABLA SEDES: TEMUCO ############
periodos=[202210,202220,202310,202320,202410,202420]
sedes="Temuco"


tabla_total_temuco=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final[tabla_final["PERIODO"]==periodo]
    tabla_auxiliar=tabla_auxiliar[tabla_auxiliar["SEDE"]==sedes]
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_temuco=pd.merge(tabla_total_temuco, aux,on="TIPO_HORARIO",how="left")


periodos=[201610,201620,201710,201720,201810,201820,201910,201920,202010,202020,202110,202120]
tabla_total_2016=pd.DataFrame({"TIPO_HORARIO":["Teoría","Laboratorio/taller","Campo Clínico","Terreno"]})
for periodo in periodos:

    tabla_auxiliar=tabla_final_antiguo[tabla_final_antiguo["PERIODO"]==periodo]
    tabla_auxiliar=tabla_auxiliar[tabla_auxiliar["SEDE"]==sedes]    
    
    
    tabla_tipo_horarios_planificadas=tabla_auxiliar.pivot_table(values=["TOTAL_SECCIONES"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_planificadas=tabla_tipo_horarios_planificadas.reset_index()
    
    
    tabla_tipo_horarios_estandar=tabla_auxiliar.pivot_table(values=["SECCIONES_ESTANDAR"],
                                        index=["TIPO_HORARIO"],
                                        #columns=["PERIODO"],
                                        aggfunc="sum")
    tabla_tipo_horarios_estandar=tabla_tipo_horarios_estandar.reset_index()
    
    
    
    tabla=pd.merge(tabla_tipo_horarios_planificadas,tabla_tipo_horarios_estandar,on="TIPO_HORARIO",how="outer")
    tabla[f"{periodo}"]=tabla["TOTAL_SECCIONES"]-tabla["SECCIONES_ESTANDAR"]
    aux=tabla[["TIPO_HORARIO",f"{periodo}"]]
    tabla_total_2016=pd.merge(tabla_total_2016, aux,on="TIPO_HORARIO",how="left")




tabla_historica_temuco=tabla_total_2016.merge(tabla_total_temuco,on="TIPO_HORARIO")










###############################STREAMLIT####################################################################################################


colormap=sns.light_palette("green", as_cmap=True)


# Ejemplo de uso en Streamlit
def main():
    
    st.title('Planificación de Sesiones Históricas')
    st.text("Resultado: Total sesiones segun estandar menos Total sesiones planificadas reales ")
    
    
    st.header('Resultados Corporativos')
    st.dataframe(tabla_corporativa_historica.style
                 .format(precision=0, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
                 ,hide_index=True)
    st.text("Estandar [2016-2021]: 45-25-1")
    st.text("Estandar [2022-2024]: 60-25-1")






    st.header('Resultados Providencia')
    st.dataframe(tabla_historica_providencia.style
                 .format(precision=0, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
                 ,hide_index=True)

    st.header('Resultados San Miguel')
    st.dataframe(tabla_historica_sanmiguel.style
                 .format(precision=0, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
                 ,hide_index=True)

    st.header('Resultados Talca')
    st.dataframe(tabla_historica_talca.style
                 .format(precision=0, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
                 ,hide_index=True)


    st.header('Resultados Temuco')
    st.dataframe(tabla_historica_temuco.style
                 .format(precision=0, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
                 ,hide_index=True)





if __name__ == '__main__':
    main()


