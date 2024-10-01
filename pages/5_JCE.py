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



#################### EXTRACCION DE LA BASE DE DATOS DESDE 2022 EN ADELANTE ###############################


server = 'svr-uautonoma-prd.database.windows.net'
database = 'db-uautonoma-prd'
username = 'sa_uautonoma'
password = 'Admin.prd.2023!'
driver = 'ODBC Driver 18 for SQL Server' 



# Establecer la conexión
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# seleccion de los programas, se descartan doctorados y magister.
programas_presupuesto=pd.read_excel("programas_presupuesto.xlsx")
programas_presupuesto=programas_presupuesto["UWVPRES_NOMBRE_PROGRAMA"].drop_duplicates().to_list()



# Función para ejecutar consultas y devolver un DataFrame
@st.cache_data
def ejecutar_consulta(query):
    return pd.read_sql(query, conn)

#consulta a la base de datos
df_base = ejecutar_consulta("SELECT * FROM STG.UWVPRES WHERE UWVPRES_TERM_CODE > 202153")
df_base=df_base.drop_duplicates()






################# BASE DE PRESUPUESTO################################
df_base_ppto=df_base[["UWVPRES_TERM_CODE","UWVPRES_CRN","UWVPRES_PROGRAMA","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_TIPO_CURSO","UWVPRES_CAMPUS","UWVPRES_SUBJ_CODE","UWVPRES_CRSE_NUMB","UWVPRES_NOMBRE_CURSO","UWVPRES_HORAS","UWVPRES_VALOR","UWVPRES_SEMANAS","UWVPRES_GRADO_DOCENTE","UWVPRES_DOCENTE_CONTRATADO"]]
df_base_ppto["TOTAL"]=df_base_ppto["UWVPRES_HORAS"]*df_base_ppto["UWVPRES_SEMANAS"]
#considero solo los programas del presupuesto:
df_base_ppto=df_base_ppto[df_base_ppto["UWVPRES_NOMBRE_PROGRAMA"].isin(programas_presupuesto)]



dist_horas=df_base_ppto.pivot_table(values=["TOTAL"],
                    index=["UWVPRES_TERM_CODE","UWVPRES_NOMBRE_PROGRAMA","UWVPRES_TIPO_CURSO","UWVPRES_CAMPUS","UWVPRES_GRADO_DOCENTE","UWVPRES_DOCENTE_CONTRATADO"],
                    aggfunc="sum")
dist_horas=dist_horas.reset_index() #devuelte la tabla dinamica a un dataframe normal

#dist_horas.to_excel("dist_horas.xlsx")

################33 analisis corporativo#############



#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_grado=dist_horas["UWVPRES_GRADO_DOCENTE"].drop_duplicates().to_list()
periodos=["202210","202220","202310","202320","202410","202420"]

#FILTRO PARA QUE SOLO TOME A LA PLANTA REGULAR
dist_horas=dist_horas[dist_horas["UWVPRES_DOCENTE_CONTRATADO"]=="Y"]

tabla_corporativa_dist=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_GRADO"]:
        
        #periodo="202410"
        
        horas=dist_horas[(dist_horas["UWVPRES_TERM_CODE"]==periodo )&(dist_horas["UWVPRES_GRADO_DOCENTE"]==tipo )]["TOTAL"].sum()
        lista_inscritos.append(horas)
    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_corporativa_dist=pd.merge(tabla_corporativa_dist,tabla_aux_inscritos,on="TIPO_GRADO",how="left")




################PROVIDENCIA #############



#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_grado=dist_horas["UWVPRES_GRADO_DOCENTE"].drop_duplicates().to_list()
periodos=["202210","202220","202310","202320","202410","202420"]
sede="Providencia"

#FILTRO PARA QUE SOLO TOME A LA PLANTA REGULAR
dist_horas=dist_horas[dist_horas["UWVPRES_DOCENTE_CONTRATADO"]=="Y"]

tabla_providencia_dist=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_GRADO"]:
        
        #periodo="202410"
        
        horas=dist_horas[(dist_horas["UWVPRES_TERM_CODE"]==periodo )&(dist_horas["UWVPRES_GRADO_DOCENTE"]==tipo )&(dist_horas["UWVPRES_CAMPUS"]==sede )]["TOTAL"].sum()
        lista_inscritos.append(horas)
    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_providencia_dist=pd.merge(tabla_providencia_dist,tabla_aux_inscritos,on="TIPO_GRADO",how="left")




################san miguel #############



#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_grado=dist_horas["UWVPRES_GRADO_DOCENTE"].drop_duplicates().to_list()
periodos=["202210","202220","202310","202320","202410","202420"]
sede="San Miguel"

#FILTRO PARA QUE SOLO TOME A LA PLANTA REGULAR
dist_horas=dist_horas[dist_horas["UWVPRES_DOCENTE_CONTRATADO"]=="Y"]

tabla_sanmiguel_dist=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_GRADO"]:
        
        #periodo="202410"
        
        horas=dist_horas[(dist_horas["UWVPRES_TERM_CODE"]==periodo )&(dist_horas["UWVPRES_GRADO_DOCENTE"]==tipo )&(dist_horas["UWVPRES_CAMPUS"]==sede )]["TOTAL"].sum()
        lista_inscritos.append(horas)
    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_sanmiguel_dist=pd.merge(tabla_sanmiguel_dist,tabla_aux_inscritos,on="TIPO_GRADO",how="left")



################ talca #############



#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_grado=dist_horas["UWVPRES_GRADO_DOCENTE"].drop_duplicates().to_list()
periodos=["202210","202220","202310","202320","202410","202420"]
sede="Talca"

#FILTRO PARA QUE SOLO TOME A LA PLANTA REGULAR
dist_horas=dist_horas[dist_horas["UWVPRES_DOCENTE_CONTRATADO"]=="Y"]

tabla_talca_dist=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_GRADO"]:
        
        #periodo="202410"
        
        horas=dist_horas[(dist_horas["UWVPRES_TERM_CODE"]==periodo )&(dist_horas["UWVPRES_GRADO_DOCENTE"]==tipo )&(dist_horas["UWVPRES_CAMPUS"]==sede )]["TOTAL"].sum()
        lista_inscritos.append(horas)
    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_talca_dist=pd.merge(tabla_talca_dist,tabla_aux_inscritos,on="TIPO_GRADO",how="left")



################ temuco #############



#tipos_de_horario=presupuesto["UWVPRES_TIPO_CURSO"].drop_duplicates().to_list()
tipos_de_grado=dist_horas["UWVPRES_GRADO_DOCENTE"].drop_duplicates().to_list()
periodos=["202210","202220","202310","202320","202410","202420"]
sede="Temuco"

#FILTRO PARA QUE SOLO TOME A LA PLANTA REGULAR
dist_horas=dist_horas[dist_horas["UWVPRES_DOCENTE_CONTRATADO"]=="Y"]

tabla_temuco_dist=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})

for periodo in periodos:
    tabla_aux_inscritos=pd.DataFrame({"TIPO_GRADO":tipos_de_grado})
    lista_inscritos=[]
    for tipo in tabla_aux_inscritos["TIPO_GRADO"]:
        
        #periodo="202410"
        
        horas=dist_horas[(dist_horas["UWVPRES_TERM_CODE"]==periodo )&(dist_horas["UWVPRES_GRADO_DOCENTE"]==tipo )&(dist_horas["UWVPRES_CAMPUS"]==sede )]["TOTAL"].sum()
        lista_inscritos.append(horas)
    
    tabla_aux_inscritos[f"{periodo}"]=pd.DataFrame(lista_inscritos)
    
    
    
    tabla_temuco_dist=pd.merge(tabla_temuco_dist,tabla_aux_inscritos,on="TIPO_GRADO",how="left")





























###############################STREAMLIT####################################################################################################


colormap=sns.light_palette("green", as_cmap=True)


# Ejemplo de uso en Streamlit
def main():
    
    st.title('Distribución Horaria de Planta Regular')
    st.text("Cantidad de Horas impartidas por tipo de grado académico")
    
    
    st.header('Resultados Corporativos')
    st.dataframe(tabla_corporativa_dist.style
                  .format({"202210":'{:,.0f}',
                           "202220":'{:,.0f}',
                           "202310":'{:,.0f}',
                           "202320":'{:,.0f}',
                           "202410":'{:,.0f}',
                           "202420":'{:,.0f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)







    st.header('Resultados Providencia')
    st.dataframe(tabla_providencia_dist.style
                  .format({"202210":'{:,.0f}',
                           "202220":'{:,.0f}',
                           "202310":'{:,.0f}',
                           "202320":'{:,.0f}',
                           "202410":'{:,.0f}',
                           "202420":'{:,.0f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)

    st.header('Resultados San Miguel')
    st.dataframe(tabla_sanmiguel_dist.style
                  .format({"202210":'{:,.0f}',
                           "202220":'{:,.0f}',
                           "202310":'{:,.0f}',
                           "202320":'{:,.0f}',
                           "202410":'{:,.0f}',
                           "202420":'{:,.0f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)

    st.header('Resultados Talca')
    st.dataframe(tabla_talca_dist.style
                  .format({"202210":'{:,.0f}',
                           "202220":'{:,.0f}',
                           "202310":'{:,.0f}',
                           "202320":'{:,.0f}',
                           "202410":'{:,.0f}',
                           "202420":'{:,.0f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)


    st.header('Resultados Temuco')
    st.dataframe(tabla_temuco_dist.style
                  .format({"202210":'{:,.0f}',
                           "202220":'{:,.0f}',
                           "202310":'{:,.0f}',
                           "202320":'{:,.0f}',
                           "202410":'{:,.0f}',
                           "202420":'{:,.0f}',
                          
                          },
                          precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["202210","202220","202310","202320","202410","202420"],axis=1)
                  ,hide_index=True)





if __name__ == '__main__':
    main()

