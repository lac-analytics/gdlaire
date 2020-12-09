# Datos

[Inicio](../../README.MD)
***

Los datos utilizados en el proyecto han sido obtenidos de las siguientes fuentes:

+ Estructura de calles: [OpenStreetMap](https://openstreetmap.org) utilizando [OSMnx](https://github.com/gboeing/osmnx)
+ Calidad del aire [Secretaría de Medio Ambiente. Jalisco](https://semadet.jalisco.gob.mx/)
+ Estaciones de Mi Macro Periférico. Obtenidas a través de la Secretaría de Obra Pública del Estado de Jalisco.

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

TODO: #35 @edgaregurrola puedes desarrollar la parte de limpieza de las mediciones?

***
Anterior: [Inicio](../../README.md)

Siguiente: [Análisis](analisis.md)
***