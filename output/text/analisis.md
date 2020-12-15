# Análisis

[Inicio](../../README.MD)
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

## 2.- Emisiones de edificios

Se realizó un cálculo de las emisiones estimadas de toneladas de CO₂ equivalente en los edificios gubernamentales aledaños a las estaciones de MiMacro Periférico con el objetivo de identificar el impacto que tienen estos espacios en el cambio climático y establecer una primera línea base que posteriormente se pueda utilizar para definir objetivos de reducción de emisiones.

### **2.1.- Cálculo de emisiones**

Debido a que no se tiene la información gubernamental abierta al público sobre el consumo energético por edificación se tuvieron que diseñar otras rutas de acceso a los datos aprovechando los datos que sí están publicados y plataformas de datos abiertos para realizar cruces de información y así estimar los valores de emisión. A continuación se detallan los pasos:

+ Localización de edificios gubernamentales: El primer paso fue obtener la ubicación de los sitios gubernamentales utilizando la base de datos georreferenciada del [Directorio Estadístico de Unidades Económicas](https://www.inegi.org.mx/app/descarga/?ti=6) y filtrando los códigos con actividades gubernamentales (931).

+ Filtrado de edificios gubernamentales: Posteriormente, fue necesario extraer los edificios gubnernamentales que sí se encontraban dentro del área de influencia (1000m) de las estaciones. Para esto se hizo un recorte de los puntos dentro de los buffers.
![Edificios gubernamentales en el área de influencia de las estaciones](../figures/ActGubernamental-EstacionesMiMacroPeriferico.png)

+ Descarga de edificaciones: Utilizando la base de datos de [OpenStreetMap](https://www.openstreetmap.org/#map=6/23.944/-102.579) y el módulo [OSMnx](https://osmnx.readthedocs.io/en/stable/) para Python se descargaron los edificios construidos en el área de influencia de las estaciones.
![Edificios en el área de influencia de las estaciones](../figures/Edificios-EstacionesMiMacroPeriferico.png)

+ Estimación del área de edificios gubernamentales: Se intentó generar un cruce de los datos del DENUE con los de OSM para obtener la información de los m² construidos en los edificios gubernamentales. Sin embargo, no se identificaron coincidencias. Por lo tanto, fue necesario estimar el área de estos espacios calculando el área promedio de los edificios que sí tenían información en las zonas de influencia, este valor (2122m²) fue utilizado en cálculos posteriores como el área de cada punto.


+ Cálculo del consumo energético: Con el dato de m² estimados de edificios gubernamentales para cada estación de MiMacro Periférico se realizó el cálculo del consumo energético, multiplicando los m² con la estimación de consumo de [Google.org Enviromental Insights Explorer](https://insights.sustainability.google/places/ChIJOwV0Q_qxKIQR7NCkjDwfR-k/buildings) para edificaciones no residenciales (144.06kWh/m²/yr).

+ Cálculo de emisiones: Por último, el consumo energético por edificio en unidades kWh/yr se multiplicó por la estimación de emisiones de CO₂ de [Google.org Enviromental Insights Explorer](https://insights.sustainability.google/places/ChIJOwV0Q_qxKIQR7NCkjDwfR-k/buildings) (0.00041423tCO₂e/kWh). Como se mencionó previamente, este valor se obtuvo para cada estación de MiMacro Periférico.

![Emisiones en edificios gubernamentales por estaciones](../figures/emisiones_edificios/EmisionesEstaciones_Mapa.png)

#### **2.1.1.- Limitantes**

Como se describió en la metodología, los datos de m² para cada edificio gubernamental fueron calculados a partir del promedio de los edificios con los que sí se contaba información en las áreas de influencia. Además, debido a que los datos de consumo energético son estimaciones de Google, se pierde el detalle que puede tener en la realidad un edificio con mayor área comparado con uno de menor.

### **2.2.- Siguientes pasos**

La información del consumo energético detallado de los edificios de gobierno puede ser abierta al público utilizando una API orientada a comunicar a la población en general acerca del impacto de la operación gubernamental en el cambio climático.

En caso de que las instancias gubernamentales no monitoreen estos datos actualmente, se considera que sería de gran utilidad definir un proyecto que lo contemple, de tal manera que se cuente con una línea base más sólida para justificar la implementación de estrategias de ahorro energético o cambio a energías renovables.

## 3.- Potencial Solar

### **3.1.- Cálculo potencial**

![Potencial solar por estaciones](../figures/potencial_solar/PotencialEstaciones_Mapa.png)

#### 3.1.1.- Limitantes

### **3.2.- Siguientes pasos**

## 4.- Emisiones de transporte

Para dimensionar el impacto que tendrá MiMacro Periférico se realizó una estimación de las emisiones por transporte en las áreas de influencia de cada estación.

### **4.1.- Cálculo contaminación**

El cálculo de las emisiones de toneladas de CO₂ equivalente por transporte en las áreas de influencia de las estaciones se realizó de la siguiente manera:

+ Descarga de vialidades: Utilizando la base de datos de [OpenStreetMap](https://www.openstreetmap.org/#map=6/23.944/-102.579) y el módulo [OSMnx](https://osmnx.readthedocs.io/en/stable/) para Python se descargaron las vialidades en el área de influencia de las estaciones.

+ Longitud de vialidades: A partir de las vialidades descargadas se realizó un recorte de aquellas que se encontraban dentro del área de influencia (1000m) de las estaciones. Posteriormente, se calculó la longitud de las vialidades (m), para esto fue necesario recalcular las longitudes de las vialidades tras realizar el recorte.
![Vialidades en área de influencia de estaciones](../figures/AreaEstudio_Vialidades.png)

+ División de estación por municipio: Con información del [Marco Geoestadístico de INEGI](https://www.inegi.org.mx/temas/mg/default.html#Descargas) se hizo una unión espacial con las estaciones para concer en qué municipio (Guadalajara, Zapopan o San Pedro Tlaquepaque) se encontraba cada una.

+ Reparto modal: Se utilizaron los repartos modales, eficiencia de los vehículos y emisiones de toneladas de CO₂ por litro de combustible de [Google.org Environmental Insights Explorer](https://insights.sustainability.google/places/ChIJOwV0Q_qxKIQR7NCkjDwfR-k/transportation) para automóviles, transporte público y motocicletas. Debido a que no se obtuvieron datos de Zapopan se realizaron promedios de los valores de San Pedro Tlaquepaque y Guadalajara.

+ Cálculo de consumo de combustible: Para cada método de transporte analizado se multiplicó la distancia en kilómetros de cada estación por el porcentaje del reparto y posteriormente por la eficiencia promedio.

+ Cálculo de emisiones: Con el consumo de litros por método de transporte se multiplicó este valor por la emisión estimada promedio por litro de combustible. Los valores de cada método de transporte se sumaron. Debido a que las emisiones son para la distancia y no tienen una temporalidad, se asumió que los datos de Google representan un día promedio. Con base en esto cada valor se multiplicó por 265, una estimiación de los días hábiles en un año.

+ Ejemplo: a continuación se muestra un ejemplo del cálculo realizado:

<p align="center">10 km en estación <em>x</em> * 0.8 (porcentaje de transporte en automóvil para Guadalajara) / 9.1 (eficiencia promedio de los automóviles) * 0.002 (emisiones en toneladas de CO₂ por litro de combustible) * 265 días hábiles</p>

![Emisiones por transporte por estaciones](../figures/emisiones_transporte/EmisionesVialidades_Mapa.png)

#### **4.1.1.- Limitantes**

Los datos que se utilizaron del reparto modal de Google representan un promedio para todo el municipio (acotando que solo se tuvo acceso a la información de Guadalajara y San Pedro Tlaquepaque), sin embargo, es posible que en las áreas de influencia de las estaciones estas sean distintas. Además, el reparto modal que se utilizó para estimar las emisiones no contempla la carga vehicular de cada vialidad y asume que esta se divide de forma uniforme en todo el municipio.

### **4.2.- Siguientes pasos**

Es posible aprovechar los datos de tráfico que tiene Google para estimar de forma más certera la carga de las vialidades en las áreas de influencia y definir una línea base de emisiones más apeagada a la realidad. Además, los embotellamientos hacen que se reduzca la eficiencia de consumo del combustible, así que no solamente se puede obtener una mejor estimación por la carga de la vialidad sino por la congestión de los vehículos en la zona.


***
Anterior: [Datos](data.md)

Siguiente: [Equipo](Equipo.md)
***