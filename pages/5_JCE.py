import streamlit as st
import pandas as pd
import seaborn as sns

corporativo=pd.read_excel("corporativo_5.xlsx")
providencia=pd.read_excel("providencia_5.xlsx")
sanmiguel=pd.read_excel("sanmiguel_5.xlsx")
talca=pd.read_excel("talca_5.xlsx")
temuco=pd.read_excel("temuco_5.xlsx")

###############################STREAMLIT####################################################################################################



colormap=sns.light_palette("green", as_cmap=True)


# Ejemplo de uso en Streamlit
def main():
    
    st.title('Distribución Horaria JCE')
    
    st.text("En las siguientas tablas se muestra la distribución de horas por tipo de horario en manos de planta regular.")
    st.divider()




    st.header('Resultados Corporativos')
    st.dataframe(corporativo.style
                 .format(precision=2, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                 ,hide_index=True)






    st.header('Resultados Providencia')
    st.dataframe(providencia.style
                 .format(precision=2, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                 ,hide_index=True)




    
    st.header('Resultados San Miguel')
    st.dataframe(sanmiguel.style
                 .format(precision=2, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                 ,hide_index=True)    
    






    st.header('Resultados Talca')
    st.dataframe(talca.style
                  .format(precision=2, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                  ,hide_index=True)





    st.header('Resultados Temuco')
    st.dataframe(temuco.style
                  .format(precision=2, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["2022","2023","2024"],axis=1)
                  ,hide_index=True)


if __name__ == '__main__':
    main()
