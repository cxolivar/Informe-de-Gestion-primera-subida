# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:17:44 2024

@author: Carmen
"""
import streamlit as st
import pyodbc
import pandas as pd
import time
import numpy as np
import seaborn as sns
import openpyxl



#################### EXTRACCION DE LA BASE DE DATOS DESDE 2022 EN ADELANTE ###############################


server = 'svr-uautonoma-prd.database.windows.net'
database = 'db-uautonoma-prd'
username = 'sa_uautonoma'
password = st.secrets["clave"]
driver = 'ODBC Driver 18 for SQL Server' 



# Establecer la conexión
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# seleccion de los programas, se descartan doctorados y magister.
programas_presupuesto=pd.read_excel("programas_presupuesto.xlsx")
programas_presupuesto=programas_presupuesto["UWVPRES_NOMBRE_PROGRAMA"].drop_duplicates().to_list()
UF=pd.DataFrame({"PERIODO":["202210","202220","202310","202320","202410","202420"],"VALOR UF":[31721,31721,35575,35575,37093,37093]})



# Función para ejecutar consultas y devolver un DataFrame
@st.cache_data
def ejecutar_consulta(query):
    return pd.read_sql(query, conn)

#consulta a la base de datos
df_base = ejecutar_consulta("SELECT * FROM STG.UWVPRES WHERE UWVPRES_TERM_CODE > 202153")
df_base=df_base.drop_duplicates()
df_base_inscritos = ejecutar_consulta("SELECT * FROM STG.UWVPLNI")







################# BASE DE PRESUPUESTO################################
df_base_ppto=df_base[["UWVPRES_TERM_CODE","UWVPRES_CRN","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_TIPO_CURSO","UWVPRES_CAMPUS","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_HORAS","UWVPRES_VALOR","UWVPRES_SEMANAS"]]
df_base_ppto["TOTAL"]=df_base_ppto["UWVPRES_HORAS"]*df_base_ppto["UWVPRES_VALOR"]*df_base_ppto["UWVPRES_SEMANAS"]
#considero solo los programas del presupuesto:
df_base_ppto=df_base_ppto[df_base_ppto["UWVPRES_NOMBRE_PROGRAMA"].isin(programas_presupuesto)]



presupuesto=df_base_ppto.pivot_table(values=["TOTAL"],
                    index=["UWVPRES_TERM_CODE","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_TIPO_CURSO","UWVPRES_CAMPUS"],
                    aggfunc="sum")
presupuesto=presupuesto.reset_index() #devuelte la tabla dinamica a un dataframe normal



####################BASE DE TOTAL SECCIONES###############################

df_base_inscritos["LLAVE"]=df_base_inscritos["UWVPLNI_TERM_CODE"]+df_base_inscritos["UWVPLNI_CRN"]


df_principal=df_base[["UWVPRES_TERM_CODE","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_AREA_PRIORITY","UWVPRES_CRN","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_CAMPUS","UWVPRES_TIPO_CURSO"]]
df_principal["INSCRITOS"]=0
df_principal["LLAVE"]=df_principal["UWVPRES_TERM_CODE"]+df_principal["UWVPRES_CRN"]

# acá se colocan el numero de inscritos y es la base que mantienen todos los nrc
df_principal=pd.merge(df_principal,df_base_inscritos,on="LLAVE")
df_principal=df_principal[["UWVPRES_TERM_CODE","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_AREA_PRIORITY","UWVPRES_CRN","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_CAMPUS","UWVPRES_TIPO_CURSO","UWVPLNI_INSCRITOS"]]
df_principal=df_principal.drop_duplicates(keep="first")


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
tabla_alumnos=pd.merge(total_inscritos,total_sesiones,on=["UWVPRES_TERM_CODE","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_AREA_PRIORITY","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_CAMPUS","UWVPRES_TIPO_CURSO"])






################33 analisis corporativo#############

#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_horario=["Sup de practica y titulación","Laboratorio/taller","Simulación de Alta","Teoría","Simulación de Baja","Ayudantía en sala","Aprendizaje Mediado"]
periodos=["202210","202220","202310","202320","202410","202420"]




tabla_corporativa_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_HORARIO"]:
        
        #periodo="202410"
        
        monto=presupuesto[(presupuesto["UWVPRES_TERM_CODE"]==periodo )&(presupuesto["UWVPRES_TIPO_CURSO"]==tipo )]["TOTAL"].sum()
        inscritos=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)]["UWVPLNI_INSCRITOS_x"].sum()
        secciones=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)]["UWVPLNI_INSCRITOS_y"].sum()
        uf=UF[UF["PERIODO"]==periodo]["VALOR UF"].reset_index(drop=True)[0] 

           
        indicador_inscritos=monto/secciones/uf
        
        lista_inscritos.append(indicador_inscritos)
        

    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_corporativa_inscritos=pd.merge(tabla_corporativa_inscritos,tabla_aux_inscritos,on="TIPO_HORARIO",how="left")



################33 ANALISIS PROVIDENCIA#############

#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_horario=["Sup de practica y titulación","Laboratorio/taller","Simulación de Alta","Teoría","Simulación de Baja","Ayudantía en sala","Aprendizaje Mediado"]
periodos=["202210","202220","202310","202320","202410","202420"]
sede="Providencia"



tabla_providencia_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_HORARIO"]:
        
        #periodo="202410"
        
        monto=presupuesto[(presupuesto["UWVPRES_TERM_CODE"]==periodo )&(presupuesto["UWVPRES_TIPO_CURSO"]==tipo )&(presupuesto["UWVPRES_CAMPUS"]==sede )]["TOTAL"].sum()
        inscritos=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)&(tabla_alumnos["UWVPRES_CAMPUS"]==sede)]["UWVPLNI_INSCRITOS_x"].sum()
        secciones=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)&(tabla_alumnos["UWVPRES_CAMPUS"]==sede)]["UWVPLNI_INSCRITOS_y"].sum()
        uf=UF[UF["PERIODO"]==periodo]["VALOR UF"].reset_index(drop=True)[0] 

           
        indicador_inscritos=monto/secciones/uf
        
        lista_inscritos.append(indicador_inscritos)
        

    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_providencia_inscritos=pd.merge(tabla_providencia_inscritos,tabla_aux_inscritos,on="TIPO_HORARIO",how="left")



################33 ANALISIS SANMIGUEL#############

#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_horario=["Sup de practica y titulación","Laboratorio/taller","Simulación de Alta","Teoría","Simulación de Baja","Ayudantía en sala","Aprendizaje Mediado"]
periodos=["202210","202220","202310","202320","202410","202420"]
sede="San Miguel"



tabla_sanmiguel_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_HORARIO"]:
        
        #periodo="202410"
        
        monto=presupuesto[(presupuesto["UWVPRES_TERM_CODE"]==periodo )&(presupuesto["UWVPRES_TIPO_CURSO"]==tipo )&(presupuesto["UWVPRES_CAMPUS"]==sede )]["TOTAL"].sum()
        inscritos=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)&(tabla_alumnos["UWVPRES_CAMPUS"]==sede)]["UWVPLNI_INSCRITOS_x"].sum()
        secciones=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)&(tabla_alumnos["UWVPRES_CAMPUS"]==sede)]["UWVPLNI_INSCRITOS_y"].sum()
        uf=UF[UF["PERIODO"]==periodo]["VALOR UF"].reset_index(drop=True)[0] 

           
        indicador_inscritos=monto/secciones/uf
        
        lista_inscritos.append(indicador_inscritos)
        

    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_sanmiguel_inscritos=pd.merge(tabla_sanmiguel_inscritos,tabla_aux_inscritos,on="TIPO_HORARIO",how="left")


################33 ANALISIS TALCA#############

#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_horario=["Sup de practica y titulación","Laboratorio/taller","Simulación de Alta","Teoría","Simulación de Baja","Ayudantía en sala","Aprendizaje Mediado"]
periodos=["202210","202220","202310","202320","202410","202420"]
sede="Talca"



tabla_talca_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_HORARIO"]:
        
        #periodo="202410"
        
        monto=presupuesto[(presupuesto["UWVPRES_TERM_CODE"]==periodo )&(presupuesto["UWVPRES_TIPO_CURSO"]==tipo )&(presupuesto["UWVPRES_CAMPUS"]==sede )]["TOTAL"].sum()
        inscritos=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)&(tabla_alumnos["UWVPRES_CAMPUS"]==sede)]["UWVPLNI_INSCRITOS_x"].sum()
        secciones=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)&(tabla_alumnos["UWVPRES_CAMPUS"]==sede)]["UWVPLNI_INSCRITOS_y"].sum()
        uf=UF[UF["PERIODO"]==periodo]["VALOR UF"].reset_index(drop=True)[0] 

           
        indicador_inscritos=monto/secciones/uf
        
        lista_inscritos.append(indicador_inscritos)
        

    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_talca_inscritos=pd.merge(tabla_talca_inscritos,tabla_aux_inscritos,on="TIPO_HORARIO",how="left")



################33 ANALISIS TEMUCO#############

#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_horario=["Sup de practica y titulación","Laboratorio/taller","Simulación de Alta","Teoría","Simulación de Baja","Ayudantía en sala","Aprendizaje Mediado"]
periodos=["202210","202220","202310","202320","202410","202420"]
sede="Temuco"



tabla_temuco_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_HORARIO":tipos_de_horario})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_HORARIO"]:
        
        #periodo="202410"
        
        monto=presupuesto[(presupuesto["UWVPRES_TERM_CODE"]==periodo )&(presupuesto["UWVPRES_TIPO_CURSO"]==tipo )&(presupuesto["UWVPRES_CAMPUS"]==sede )]["TOTAL"].sum()
        inscritos=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)&(tabla_alumnos["UWVPRES_CAMPUS"]==sede)]["UWVPLNI_INSCRITOS_x"].sum()
        secciones=tabla_alumnos[(tabla_alumnos["UWVPRES_TERM_CODE"]==periodo)&(tabla_alumnos["UWVPRES_TIPO_CURSO"]==tipo)&(tabla_alumnos["UWVPRES_CAMPUS"]==sede)]["UWVPLNI_INSCRITOS_y"].sum()
        uf=UF[UF["PERIODO"]==periodo]["VALOR UF"].reset_index(drop=True)[0] 

           
        indicador_inscritos=monto/secciones/uf
        
        lista_inscritos.append(indicador_inscritos)
        

    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_temuco_inscritos=pd.merge(tabla_temuco_inscritos,tabla_aux_inscritos,on="TIPO_HORARIO",how="left")

























###############################STREAMLIT####################################################################################################


colormap=sns.light_palette("green", as_cmap=True)


# Ejemplo de uso en Streamlit
def main():
    
    st.title('Costo Secciones por Tipo de Horario')
    st.text("Resultado: Total Presupuesto divido la cantidad de inscritos (valores en UF considerando el valor del 31 de marzo)")
    
    
    st.header('Resultados Corporativos')
    st.dataframe(tabla_corporativa_inscritos.style
                  .format({"202210":'{:,.2f}',
                           "202220":'{:,.2f}',
                           "202310":'{:,.2f}',
                           "202320":'{:,.2f}',
                           "202410":'{:,.2f}',
                           "202420":'{:,.2f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)







    st.header('Resultados Providencia')
    st.dataframe(tabla_providencia_inscritos.style
                  .format({"202210":'{:,.2f}',
                           "202220":'{:,.2f}',
                           "202310":'{:,.2f}',
                           "202320":'{:,.2f}',
                           "202410":'{:,.2f}',
                           "202420":'{:,.2f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)

    st.header('Resultados San Miguel')
    st.dataframe(tabla_sanmiguel_inscritos.style
                  .format({"202210":'{:,.2f}',
                           "202220":'{:,.2f}',
                           "202310":'{:,.2f}',
                           "202320":'{:,.2f}',
                           "202410":'{:,.2f}',
                           "202420":'{:,.2f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)

    st.header('Resultados Talca')
    st.dataframe(tabla_talca_inscritos.style
                  .format({"202210":'{:,.2f}',
                           "202220":'{:,.2f}',
                           "202310":'{:,.2f}',
                           "202320":'{:,.2f}',
                           "202410":'{:,.2f}',
                           "202420":'{:,.2f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)


    st.header('Resultados Temuco')
    st.dataframe(tabla_temuco_inscritos.style
                  .format({"202210":'{:,.2f}',
                           "202220":'{:,.2f}',
                           "202310":'{:,.2f}',
                           "202320":'{:,.2f}',
                           "202410":'{:,.2f}',
                           "202420":'{:,.2f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)





if __name__ == '__main__':
    main()

