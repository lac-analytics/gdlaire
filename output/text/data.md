# [Calidad del aire en Guadalajara](../../README.MD)

## Datos

Los datos utilizados en el proyecto han sido obtenidos de las siguientes fuentes:

+ Estructura de calles: [OpenStreetMap](https://openstreetmap.org) utilizando [OSMnx](https://github.com/gboeing/osmnx)
+ Calidad del aire [Secretaría de Medio Ambiente. Jalisco](https://semadet.jalisco.gob.mx/)
+ Estaciones de Mi Macro Periférico. Obtenidas a través de la Secretaría de Obra Pública del Estado de Jalisco.

### Origen

La red vial se obtuvo con el script [01-download-graph.py](../../scripts/01-download-graph.py) que descarga la red y guarda las tablas de nodos y enlaces en la base de datos creada para el proyecto.

Los datos de calidad del aire y las estaciones de Mi Macro Periférico fueron agregadas a la base de datos utilizando el script [00-gdf-to-db.py](../../scripts/00-gdf-to-db.py) que toma un shapefile o geoJSON, lo lee con GeoPandas y crea la tabla correspondiente en la base de datos.

### Limpieza

**Estaciones.** La base de datos con las estaciones de Mi Macro Periférico contenía el polígono de la estación, para el proyecto se está trabajando con el punto central de cada estación. Fue necesario remover la información extra antes de subir los datos a la base de datos, este proceso fue hecho de manera manual utilizando [QGIS](https://qgis.org), por lo que no se tiene un script para replicar la limpieza de estos datos.

**Mediciones de calidad del aire.**

Todo: @edgaregurrola Puedes desarrollar aquí? Gracias!
