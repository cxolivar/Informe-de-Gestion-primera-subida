import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go


corporativo=pd.read_excel("corporativo.xlsx")
providencia=pd.read_excel("providencia.xlsx")
sanmiguel=pd.read_excel("sanmiguel.xlsx")
talca=pd.read_excel("talca.xlsx")
temuco=pd.read_excel("temuco.xlsx")

def grafico_cascada(archivo,tipo):

    corporativo=archivo
    tipo_horario=tipo
    indice=corporativo[corporativo["TIPO_HORARIO"]==tipo_horario].index[0]
    
    x=list(corporativo.columns)
    x_primer=x.pop(0)
    
    y=corporativo.iloc[indice]
    y=y.to_list()
    y_primer=y.pop(0)
    
    maxy=max(y)
    miny=min(y)
    
    
    # Creamos una lista vacía para almacenar las diferencias
    diferencias = [y[0]]  # Agregamos el primer valor directamente
    
    # Iteramos a partir del segundo elemento y calculamos las diferencias
    for i in range(1, len(y)):
        diferencia = y[i] - y[i-1]
        diferencias.append(diferencia)
    
    y_texto=[round(num,2) for num in diferencias]
    
    fig = go.Figure(go.Waterfall(
        name = "2014",
        orientation = "v",
        measure = ["relative", "relative", "relative"],
        x = x,
        textposition = "outside",
        text = y_texto,
        y = diferencias,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title = tipo_horario,
        xaxis = dict(
            type = "category"
        ),
        yaxis=dict(
            range=[miny*0.9, maxy*1.1]  # Ajusta el rango mínimo y máximo
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)










###############################STREAMLIT####################################################################################################



colormap=sns.light_palette("green", as_cmap=True)


# Ejemplo de uso en Streamlit
def main():
    st.set_page_config(layout="wide")
    st.title('Planificación de Sesiones Históricas')
    st.text("Las siguientes tablas muestran la diferencia entre el total de sesiones planificadas ") 
    st.text("con las sesiones que se deberian haber planificado según el estandar de los cuadros de docencia. ")
    st.text("Para esto se tomó la demanda estudiantil por periodo y se le aplicó el estandar definidos en los cuadros")

    st.divider()
    st.text("En general el estandar se define con 60 estudiantes en secciones Teóricas, 23 estudiantes para Laboratorio")
    st.text("y 1 estudiante para secciones terreno / campo clínico.")
    st.text("Existen asignaturas que tienen composiciones especiales que tambien fueron consideradas.")
    
    
    # st.header('Resultados Corporativos')


    
    # st.dataframe(corporativo.style
    #               .format(precision=0, thousands=".", decimal=",")
    #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    #               ,hide_index=True)

    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Corporativos')
        st.dataframe(corporativo.style
                     .format(precision=0, thousands=".", decimal=",")
                     .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                     ,hide_index=True)

    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno']
        tipo = st.selectbox('', opciones,key="sel")

        
        # Crear un estado inicial
        if 'mostrar_contenido' not in st.session_state:
            st.session_state.mostrar_contenido = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="corporativo"):
            st.session_state.mostrar_contenido = not st.session_state.mostrar_contenido
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido:
            grafico_cascada(corporativo,tipo) 
             



    
    # st.header('Resultados Providencia')
    # st.dataframe(tabla_sede_periodo(tabla_final,"Providencia").style
    #               .format(precision=0, thousands=".", decimal=",")
    #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    #               ,hide_index=True)



    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Providencia')
        st.dataframe(providencia.style
                     .format(precision=0, thousands=".", decimal=",")
                     .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                     ,hide_index=True)

    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno']
        tipo = st.selectbox('', opciones,key="sel2")
        # Crear un estado inicial
        if 'mostrar_contenido2' not in st.session_state:
            st.session_state.mostrar_contenido2 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="providencia"):
            st.session_state.mostrar_contenido2 = not st.session_state.mostrar_contenido2
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido2:
            grafico_cascada(providencia,tipo) 



    # st.header('Resultados San Miguel')
    # st.dataframe(tabla_sede_periodo(tabla_final,"San Miguel").style
    #               .format(precision=0, thousands=".", decimal=",")
    #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    #               ,hide_index=True)


    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados San Miguel')
        st.dataframe(sanmiguel.style
                     .format(precision=0, thousands=".", decimal=",")
                     .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                     ,hide_index=True)    
    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno']
        tipo = st.selectbox('', opciones,"sel3")
        # Crear un estado inicial
        if 'mostrar_contenido3' not in st.session_state:
            st.session_state.mostrar_contenido3 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="sanmiguel"):
            st.session_state.mostrar_contenido3 = not st.session_state.mostrar_contenido3
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido3:
            grafico_cascada(sanmiguel,tipo) 
    

    # st.header('Resultados Talca')
    # st.dataframe(tabla_sede_periodo(tabla_final,"Talca").style
    #               .format(precision=0, thousands=".", decimal=",")
    #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    #               ,hide_index=True)



    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Talca')
        st.dataframe(talca.style
                      .format(precision=0, thousands=".", decimal=",")
                      .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                      ,hide_index=True)

    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno']
        tipo = st.selectbox('', opciones,"sel4")
        # Crear un estado inicial
        if 'mostrar_contenido4' not in st.session_state:
            st.session_state.mostrar_contenido4 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="talca"):
            st.session_state.mostrar_contenido4 = not st.session_state.mostrar_contenido4
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido4:
            grafico_cascada(talca,tipo) 


    # # st.header('Resultados Temuco')
    # # st.dataframe(tabla_sede_periodo(tabla_final,"Temuco").style
    # #               .format(precision=0, thousands=".", decimal=",")
    # #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    # #               ,hide_index=True)

    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Temuco')
        st.dataframe(temuco.style
                      .format(precision=0, thousands=".", decimal=",")
                      .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                      ,hide_index=True)

    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno']
        tipo = st.selectbox('', opciones,"sel5")
        # Crear un estado inicial
        if 'mostrar_contenido5' not in st.session_state:
            st.session_state.mostrar_contenido5 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="temuco"):
            st.session_state.mostrar_contenido5 = not st.session_state.mostrar_contenido5
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido5:
            grafico_cascada(temuco,tipo) 


if __name__ == '__main__':
    main()



