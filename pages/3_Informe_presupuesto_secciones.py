import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go

corporativo=pd.read_excel("corporativo_3.xlsx")
providencia=pd.read_excel("providencia_3.xlsx")
sanmiguel=pd.read_excel("sanmiguel_3.xlsx")
talca=pd.read_excel("talca_3.xlsx")
temuco=pd.read_excel("temuco_3.xlsx")


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
    st.title('Costo de inscritos (UF)')

    st.text("En las siguientas tablas se muestra el resultado del total prespuesto dividido por la cantidad de alumnos inscritos")
    st.text("El valor de la UF considerada corresponde a la del 31 de marzo")
    st.divider()
    
    


    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Corporativos')
        st.dataframe(corporativo.style
                     .format(precision=2, thousands=".", decimal=",")
                     .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                     ,hide_index=True)
    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno','Sup de practica y titulación','Simulación de Alta','Simulación de Baja','Ayudantía en sala','Aprendizaje Mediado']
        tipo = st.selectbox('', opciones,key="sel11")
                
        if 'mostrar_contenido11' not in st.session_state:
            st.session_state.mostrar_contenido11 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="corporativo"):
            st.session_state.mostrar_contenido11 = not st.session_state.mostrar_contenido11
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido11:
            
            grafico_cascada(corporativo,tipo) 





    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Providencia')
        st.dataframe(providencia.style
                     .format(precision=2, thousands=".", decimal=",")
                     .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                     ,hide_index=True)

    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno','Sup de practica y titulación','Simulación de Alta','Simulación de Baja','Ayudantía en sala','Aprendizaje Mediado']
        tipo = st.selectbox('', opciones,key="sel12")
                
        if 'mostrar_contenido12' not in st.session_state:
            st.session_state.mostrar_contenido12 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="providencia"):
            st.session_state.mostrar_contenido12 = not st.session_state.mostrar_contenido12
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido12:
            
            grafico_cascada(providencia,tipo) 



    col1,col2= st.columns(2)
    
    with col1:  
        st.header('Resultados San Miguel')
        st.dataframe(sanmiguel.style
                     .format(precision=2, thousands=".", decimal=",")
                     .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                     ,hide_index=True)    
    
    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno','Sup de practica y titulación','Simulación de Alta','Simulación de Baja','Ayudantía en sala','Aprendizaje Mediado']
        tipo = st.selectbox('', opciones,key="sel13")
                
        if 'mostrar_contenido13' not in st.session_state:
            st.session_state.mostrar_contenido13 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="sanmiguel"):
            st.session_state.mostrar_contenido13 = not st.session_state.mostrar_contenido13
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido13:
            
            grafico_cascada(sanmiguel,tipo) 



    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Talca')
        st.dataframe(talca.style
                      .format(precision=2, thousands=".", decimal=",")
                      .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                      ,hide_index=True)

    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno','Sup de practica y titulación','Simulación de Alta','Simulación de Baja','Ayudantía en sala','Aprendizaje Mediado']
        tipo = st.selectbox('', opciones,key="sel14")
                
        if 'mostrar_contenido14' not in st.session_state:
            st.session_state.mostrar_contenido14 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="talca"):
            st.session_state.mostrar_contenido14 = not st.session_state.mostrar_contenido14
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido14:
            
            grafico_cascada(talca,tipo) 




    col1,col2= st.columns(2)


    with col1:
        st.header('Resultados Temuco')
        st.dataframe(temuco.style
                      .format(precision=2, thousands=".", decimal=",")
                      .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                      ,hide_index=True)

    with col2:
        opciones = ['Teoría', 'Laboratorio/taller', 'Campo Clínico', 'Terreno','Sup de practica y titulación','Simulación de Alta','Simulación de Baja','Ayudantía en sala','Aprendizaje Mediado']
        tipo = st.selectbox('', opciones,key="sel15")
                
        if 'mostrar_contenido15' not in st.session_state:
            st.session_state.mostrar_contenido15 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="tamuco"):
            st.session_state.mostrar_contenido15 = not st.session_state.mostrar_contenido15
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido15:
            
            grafico_cascada(temuco,tipo) 




if __name__ == '__main__':
    main()
