import streamlit as st
import pandas as pd
import seaborn as sns

corporativo=pd.read_excel("corporativo.xlsx")
providencia=pd.read_excel("providencia.xlsx")
sanmiguel=pd.read_excel("sanmiguel.xlsx")
talca=pd.read_excel("talca.xlsx")
temuco=pd.read_excel("temuco.xlsx")

###############################STREAMLIT####################################################################################################



colormap=sns.light_palette("green", as_cmap=True)


# Ejemplo de uso en Streamlit
def main():
    
    st.title('Planificación de Sesiones Históricas')
    st.text("Las siguientes tablas muestran la diferancia entre el total de sesiones planificadas comparadas) 
    st.text("con las sesiones que se deberian haber planificadas segun el estandar de los cuadros de docencia. ")
    st.text("Para esto se tomó la demanda estudiantil por periodo y se le aplicó el el estandar por CD")
    
    
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



