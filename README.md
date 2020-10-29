# Calidad del aire en corredor Mi Macro Periferico Guadalajara

La idea de este repositorio es generar una línea base para comparar la calidad del aire en las estaciones de Mi Macro Periférico, como parte del proyecto [PIP para una ciudad del futuro.](https://www.facebook.com/pipciudadfuturo/)

## Estructura

La estructura de los folders de este proyecto es:

```
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── output            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures       <- Generated graphics and figures to be used in reporting
|   └── text          <- Reports
│
└── aqiGDL             <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── data.py        <- Scripts to download or generate data
│   │
│   ├── analysis.py    <- Scripts to analyse the data
│   │
│   └── visualization.py  <- Scripts to create exploratory and results oriented visualizations
│
└── scripts           <- Python scripts to run the analysis and produce the outputs
```

## Memoria del proceso

1. [Datos](output/text/data.md)
1. [Análisis](output/text/analisis.md)
