import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go


corporativo=pd.read_excel("corporativo_5.xlsx")
providencia=pd.read_excel("providencia_5.xlsx")
sanmiguel=pd.read_excel("sanmiguel_5.xlsx")
talca=pd.read_excel("talca_5.xlsx")
temuco=pd.read_excel("temuco_5.xlsx")

def grafico_cascada(archivo,tipo):

    corporativo=archivo
    tipo_horario=tipo
    indice=corporativo[corporativo["TIPO_GRADO"]==tipo_horario].index[0]
    
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
                
        if 'mostrar_contenido21' not in st.session_state:
            st.session_state.mostrar_contenido21 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="corporativo"):
            st.session_state.mostrar_contenido21 = not st.session_state.mostrar_contenido21
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido21:
            
            grafico_cascada(corporativo,"Doctorado") 





    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Providencia')
        st.dataframe(providencia.style
                     .format(precision=2, thousands=".", decimal=",")
                     .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                     ,hide_index=True)

    with col2:
                
        if 'mostrar_contenido22' not in st.session_state:
            st.session_state.mostrar_contenido22 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="providencia"):
            st.session_state.mostrar_contenido22 = not st.session_state.mostrar_contenido22
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido22:
            
            grafico_cascada(providencia,"Doctorado") 



    col1,col2= st.columns(2)
    
    with col1:  
        st.header('Resultados San Miguel')
        st.dataframe(sanmiguel.style
                     .format(precision=2, thousands=".", decimal=",")
                     .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                     ,hide_index=True)    
    
    with col2:
                
        if 'mostrar_contenido23' not in st.session_state:
            st.session_state.mostrar_contenido23 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="sanmiguel"):
            st.session_state.mostrar_contenido23 = not st.session_state.mostrar_contenido23
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido23:
            
            grafico_cascada(sanmiguel,"Doctorado") 



    col1,col2= st.columns(2)

    with col1:
        st.header('Resultados Talca')
        st.dataframe(talca.style
                      .format(precision=2, thousands=".", decimal=",")
                      .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                      ,hide_index=True)

    with col2:
                
        if 'mostrar_contenido24' not in st.session_state:
            st.session_state.mostrar_contenido24 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="talca"):
            st.session_state.mostrar_contenido24 = not st.session_state.mostrar_contenido24
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido24:
            
            grafico_cascada(talca,"Doctorado") 




    col1,col2= st.columns(2)


    with col1:
        st.header('Resultados Temuco')
        st.dataframe(temuco.style
                      .format(precision=2, thousands=".", decimal=",")
                      .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                      ,hide_index=True)

    with col2:
                
        if 'mostrar_contenido25' not in st.session_state:
            st.session_state.mostrar_contenido25 = False
        
        # Crear un botón
        if st.button('Mostrar graficos',key="tamuco"):
            st.session_state.mostrar_contenido25 = not st.session_state.mostrar_contenido25
        
        # Mostrar el contenido si el estado es True
        if st.session_state.mostrar_contenido25:
            
            grafico_cascada(temuco,"Doctorado") 




if __name__ == '__main__':
    main()
