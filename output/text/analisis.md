# Análisis

[Línea Base contaminantes](../../README.MD)
***

En esta sección se detallan los análisis que se realizaron a los datos y la forma en la que se trabajó (ver [Datos](data.md) para una revisión de donde vienen los datos y su procesamiento). Se realizaron tres análisis para tener una línea base de los contaminantes y potencial solar en las estaciones de Mi Macro Periférico.

## 1.- Calidad del aire

Con el objetivo de realizar una línea base para la medición de contaminantes en las estaciones del sistema BRT Mi Macro Periférico, diseñamos una metodología que nos permitiera estimar la calidad del aire en las 46 estaciones del sistema a partir de bases de datos existentes.

El primer paso fue investigar los datos y opciones de interacción con la plataforma de [Google.org Environmental Insights Explorer](https://insights.sustainability.google/), la plataforma tiene datos sobre emisiones de contaminantes y calidad del aire a nivel municipal, sin embargo, estos datos no pueden ser utilizados para estimar la contaminación a nivel de las estaciones del sistema BRT ya que las dinámicas de calidad del aire varían a lo largo del territorio.

Para subsanar la falta de datos granulares, se utilizaron los datos de las estaciones de monitoreo de calidad del aire del Área Metropolitana de Guadalajara como punto de partida. El procedimiento para la interpolación fue el siguiente:

1. Descarga de plano base de Guadalajara  
1. Ubicación de estaciones de Mi Macro Periférico  
1. Ubicción de las estaciones de monitoreo.

A partir de las ubicaciones generamos dos interpolaciones:

1. Interpolación en retícula que cubre el área de las estaciones del sistema estatal de monitoreo y las estaciones de Mi Macro Periférico.
1. Interpolación de valores de contaminantes en las estaciones de monitoreo. El código que se utilizó está disponible en [08-interpolate-mimacro.py](../../scripts/08-interpolate-mimacro.py)

### **1.1.- Interpolación en retícula**

El resultado de la primera interpolación nos permitió crear visualizaciones para entender las dinámicas de calidad del aire en la zona de estudio como la que se muestra a continuación:

![Valores IMECA PM10 1 Enero 2019](../gif/IMECA_PM10_2019-01-01_24h_200ms.gif)

Esta visualización (y las disponibles en la carpeta [gif](../gif))nos permite observar como varía la calidad del aire en las diferentes zonas de la ciudad a partir de utilizar solamente los datos disponibles de las estaciones de monitoreo. Si bien no se consideran factores como la disperción de contaminantes por viento y otros factores climáticos, la interpolación de datos permite tener un estimado de los niveles de contaminantes de manera granular para la ciudad.

### **1.2.- Interpolación por estaciones**

La segunda interpolación de los valores la realizamos sobre las estaciones de Mi Macro Periférico, para obtener los valores históricos en cada estaciones y mostrar una línea base histórica de los niveles de contaminación anteriores a la entrada en marcha del sistema de transporte masivo.

![Estación Terminal Sur](../figures/estmacro/1_2014-01-01_2019-12-31.png)

Para cada una de las estaciones realizamos el cálculo de su línea base (disponibles en la carpeta [estmacro](../figures/estmacro)), el cual, en un panel, muestra la ubicación de la estación, y los niveles de contaminación (promedio semanal) del primero de Enero del 2014 al 31 de Diciembre del 2019. Al incluir un espectro de cinco años, nos permite observar la tendencia y ciclos de los contaminantes analizados.

Con esta información es posible tener un punto de partida para el análisis de los nuevos datos que se contemplan recabar como parte del proyecto PIP Ciudad Futuro.

### **1.3.- Siguientes pasos**

Esta etapa consistió en utilizar los datos disponibles de las estaciones del Sistema de Monitoreo Atmosférico de Jalisco. Sin embargo, para afinar la medición y línea de monitoreo de en las estaciones se sugieren diversas rutas de acción:

+ **API calidad del aire.** Para facilitar el uso de los datos públicos de calidad del aire, se sugiere el desarrollo de una interfaz de programación (API) para la consulta directa de los datos.

+ **Datos Google.org.** La plataforma Environmental Insights Explorer de Google.org ofrece la función de revisar la metodología que utilizaron para los cácluos ambientales. Sin embargo, no hay acceso a los datos georeferenciados utilizados para el cálculo de sus indicadores. Sería necesario contar con los datos más granulares posibles para contrastar y mejorar los resultados obtenidos.

## 2.- Contaminación edificios

## 3.- Potencial Solar

### **3.1.- Cálculo potencial**

![Potencial solar por estaciones](../figures/potencial_solar/PotencialEstaciones_Mapa.png)

#### 3.1.1.- Limitantes

### **3.2.- Siguientes pasos**

