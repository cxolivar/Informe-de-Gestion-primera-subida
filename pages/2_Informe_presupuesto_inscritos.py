import streamlit as st
import pandas as pd
import seaborn as sns

corporativo=pd.read_excel("corporativo_2.xlsx")
providencia=pd.read_excel("providencia_2.xlsx")
sanmiguel=pd.read_excel("sanmiguel_2.xlsx")
talca=pd.read_excel("talca_2.xlsx")
temuco=pd.read_excel("temuco_2.xlsx")

###############################STREAMLIT####################################################################################################



colormap=sns.light_palette("green", as_cmap=True)


# Ejemplo de uso en Streamlit
def main():
    
    st.title('Planificación de Sesiones Históricas')
    st.text("Resultado: Total sesiones segun estandar menos Total sesiones planificadas reales ")
    
    
    # st.header('Resultados Corporativos')
    # st.dataframe(corporativo.style
    #               .format(precision=0, thousands=".", decimal=",")
    #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    #               ,hide_index=True)



    st.header('Resultados Corporativos')
    st.dataframe(corporativo.style
                 .format(precision=0, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                 ,hide_index=True)

    st.text("Estandar  60-25-1")


    # st.header('Resultados Providencia')
    # st.dataframe(tabla_sede_periodo(tabla_final,"Providencia").style
    #               .format(precision=0, thousands=".", decimal=",")
    #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    #               ,hide_index=True)




    st.header('Resultados Providencia')
    st.dataframe(providencia.style
                 .format(precision=0, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                 ,hide_index=True)




    # st.header('Resultados San Miguel')
    # st.dataframe(tabla_sede_periodo(tabla_final,"San Miguel").style
    #               .format(precision=0, thousands=".", decimal=",")
    #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    #               ,hide_index=True)
    
    st.header('Resultados San Miguel')
    st.dataframe(sanmiguel.style
                 .format(precision=0, thousands=".", decimal=",")
                 .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                 ,hide_index=True)    
    

    # st.header('Resultados Talca')
    # st.dataframe(tabla_sede_periodo(tabla_final,"Talca").style
    #               .format(precision=0, thousands=".", decimal=",")
    #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    #               ,hide_index=True)





    st.header('Resultados Talca')
    st.dataframe(talca.style
                  .format(precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                  ,hide_index=True)


    # # st.header('Resultados Temuco')
    # # st.dataframe(tabla_sede_periodo(tabla_final,"Temuco").style
    # #               .format(precision=0, thousands=".", decimal=",")
    # #               .background_gradient(cmap=colormap,subset=["201610","201620","201710","201720","201810","201820","201910","201920","202010","202020","202110","202120","202210","202220","202310","202320","202410","202420"],axis=1)
    # #               ,hide_index=True)


    st.header('Resultados Temuco')
    st.dataframe(temuco.style
                  .format(precision=0, thousands=".", decimal=",")
                  .background_gradient(cmap=colormap,subset=["2016","2017","2018","2019","2020","2021","2022","2023","2024"],axis=1)
                  ,hide_index=True)


if __name__ == '__main__':
    main()
