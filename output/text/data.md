# Datos

[Inicio](../../README.md)
***

Los datos utilizados en el proyecto han sido obtenidos de las siguientes fuentes:

+ Estructura de calles: [OpenStreetMap](https://openstreetmap.org) utilizando [OSMnx](https://github.com/gboeing/osmnx)
+ Calidad del aire [Secretaría de Medio Ambiente. Jalisco](https://semadet.jalisco.gob.mx/)
+ Estaciones de Mi Macro Periférico. Obtenidas a través de la Secretaría de Obra Pública del Estado de Jalisco.
+ Estaciones de monitoreo [Sistema Nacional de Información de la Calidad del Aire](https://sinaica.inecc.gob.mx/)

## Origen

A continuación se describe el origen de las bases de datos utilizadas para el desarrollo del proyecto.

### Red Vial

La red vial se obtuvo con el script [01-download-graph.py](../../scripts/01-download-graph.py) que descarga la red y guarda las tablas de nodos y enlaces en la base de datos creada para el proyecto.

### Calidad del Aire

Los datos de calidad del aire y las estaciones de Mi Macro Periférico fueron agregadas a la base de datos utilizando el script [00-gdf-to-db.py](../../scripts/00-gdf-to-db.py) que toma un shapefile o geoJSON, lo lee con GeoPandas y crea la tabla correspondiente en la base de datos.

### Actividades económicas

Los datos necesarios para identificar los edificos con actividades gubernamentales fueron tomados del [Directorio Estadístico Nacional de Unidades Económicas](https://www.inegi.org.mx/app/mapa/denue/), aplicando un buffer de las estaciones del sistema Mi Macro Periférico se identificaron las ubicaciones de las actividades gubernamentales que estuvieran dentro del área de estudio.

### Desplante edificaciones

Para el cálculo de potencial solar fue necesario contar con el desplante de las edificaciones en las zonas de interés. Se utilizó OpenStreetMap como plano base, y utilizando OSMnx se descargaron los desplantes de los edificos dentro de las áreas de estudio.

### Estaciones Mi Macro Periférico

La base de datos fue proporcionada por parte de la Secretaría de Infraestructura y Obra Pública del Estado de Jalisco dentro de un archivo KML.

## Limpieza

Algunas de las bases de datos requirieron limpieza para que fueran utilizables en el proyecto, a continuación se detallan los pasos seguidos.

### Estaciones Mi Macro Periférico

La base de datos con las estaciones de Mi Macro Periférico contenía el polígono de la estación, para el proyecto se está trabajando con el punto central de cada estación. Fue necesario remover la información extra antes de subir los datos a la base de datos, este proceso fue hecho de manera manual utilizando [QGIS](https://qgis.org), por lo que no se tiene un script para replicar la limpieza de estos datos.

### Mediciones de calidad del aire

El formato de las bases de datos de la Secretaría de Medio Ambiente y Desarrollo Territorial (Semadet) es .xlsx, estas tablas tienen matrices con hojas de cálculo por cada estación de monitoreo, se cuenta con infomración 10 estaciones en total, y en cada hoja hay columnas para la fecha, hora, contaminantes y variables meteorológicas. Algunas de las dificultades para el uso de la información que se identificaron fueron que hay celdas con valores nulos, celdas sin fecha, sin hora o con formato incorrecto, columnas con nombres distintos para los contaminantes (por ejemplo, O3 en una base de datos y Ozono en otra), y hojas de cálculo con nombres distintos para cada estación (por ejemplo, Las Águilas para un año y Águilas en otro). 

Para el tratamiento, se generaron nuevos DataFrames para cada año con la información de todas las fechas, horarios, contaminantes y estaciones en una sola hoja, de forma que fuera más sencillo y claro acceder a los valores individuales. El nuevo DataFrame cuenta con 13 columnas y 43,800 filas, ya que son 5 contaminantes por cada hora. Las columnas contienen las claves de las estaciones en lugar de utilizar sus nombres (por ejemplo, se colocó TLA para Tlaquepaque, VAL para Vallarta, etc.).

Para generar la base de datos fue necesario identificar y corregir los huecos en las fechas, tomando como verdadera la fecha previa (que anteriormente había sido corregida), solucionar errores en formatos de fechas y horas, identificando si estaban registradas como texto o número, corregir nombres de columnas y de hojas de cálculo para estandarizarlos, entre otros. Además, los nuevos DataFrames fueron creados con todas las fechas, parámetros y estaciones, dejando la información de concentraciones como nulos, de esta manera se redujo la posibilidad de problemas por huecos en la información. A su vez, esto hizo que, en caso de que un dato no se encontrara en la tabla original, el valor se conservó como nulo. Cada tabla fue guardada posteriormente en formato csv.

Las tablas se unieron con las bases de datos de las estaciones del Sistema Nacional de Información de la Calidad del Aire (Sinaica) para integrar las coordenadas de las estaciones. Para hacer esto se unieron las claves únicas de las estaciones en ambas bases de datos. Posteriormente, se reestructuraron los DataFrames y se unieron todos los años en una sola tabla, esta tiene una estructura de fecha, hora, parámetro (contaminante), concentración, longitud y latitud. 

***
Anterior: [Inicio](../../README.md)

Siguiente: [Análisis](analisis.md)
***