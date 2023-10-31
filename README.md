# Proyecto Individual 1 - Sistema de Recomendación de Videojuegos para Steam

<p align="center">
  <img src="images/image (2).png" width="400" alt="Texto alternativo si la imagen no carga">
</p>


En este proyecto se planto la tarea de crear un sistema de recomendacion de videojuegos para la plataforma de Steam. Este trabajo se realizo desde cero, Se logro ofrecer una solucion completa que involucra desde la ingenieria de los datos, hasta el despliegue de una API utilizando la libreria FastAPI. El objetivo de este proyecto es proporcionar a los usuarios una herramienta efectiva para descubrir nuevos juegos en base a un analisis de sentimiento, informacion de los desarrolladores, interaccion de los usuarios y un modelo de machine learning.

## Descripción del Proyecto

El sistema se construye en dos etapas principales:

### 1. Ingeniería de Datos y Desarrollo de API

- **ETL:** Se realizó la limpieza inicial y formateo del dataset para su correcta lectura. Se implementó un análisis de sentimiento con NLP para la creación de la columna 'opinion', permitiendo la optimización del rendimiento de la API y el entrenamiento de los modelos de machine learning.

- **API con FastAPI:** Se propuso y desarrolló una API usando FastAPI que ofrece diversas consultas a los datos disponibles, brindando información sobre desarrolladores, usuarios, géneros y juegos.

- **Deployment:** La API se encuentra desplegada y disponible para ser consumida desde la web, utilizando el servicio Render y siguiendo el tutorial disponible en el repositorio.

### 2. EDA y Modelos de Machine learning

- **Analisis exploratorio:** Se realizó un análisis exploratorio de los datos para comprender mejor las relaciones entre las variables del dataset, identificar outliers, anomalías y patrones interesantes para un análisis posterior.

- **Modelos de Recomendación:** Se implementó al menos uno de dos tipos de sistemas de recomendación: ítem-ítem y usuario-ítem. Estos modelos permiten sugerir juegos similares basados en la similitud entre ítems o usuarios.

## Funcionalidades Principales de la API

<p align="center">
  <img src='images/image (1).jpg' width="400" alt="Texto alternativo si la imagen no carga">
</p>

La API proporciona las siguientes funciones:

`developer(desarrollador)` - Esta función toma como entrada una cadena de texto que representa el nombre de un desarrollador. Busca en un DataFrame que contiene información sobre juegos y filtra los datos para ese desarrollador. Luego, recorre las fechas de lanzamiento únicas y recopila información sobre cuántos juegos se lanzaron en cada año y cuántos de ellos eran gratuitos. Finalmente, devuelve un diccionario con dos claves: 'Cantidad de Items' y 'Contenido Free', cada una de las cuales contiene un diccionario con los años como claves y la cantidad de juegos o juegos gratuitos como valores.

`userdata(User_id)` - Esta función toma como entrada una cadena de texto que representa un usuario. Primero verifica si el usuario existe en un DataFrame que contiene información sobre los usuarios y sus juegos. Luego, lee un archivo CSV en bloques y busca el usuario en cada bloque. Una vez que encuentra al usuario, calcula la cantidad de dinero que ha gastado, la cantidad de juegos que tiene y el porcentaje de juegos que ha recomendado. Finalmente, devuelve un diccionario con esta información.

`best_developer_year(año)` - Esta función toma como entrada un entero que representa un año. Lee un archivo CSV que contiene información sobre los desarrolladores y la cantidad de juegos que lanzaron cada año. Filtra los datos para el año dado y luego devuelve un diccionario con la información del 'Top 1', 'Top 2' y 'Top 3' de los desarrolladores que lanzaron más juegos ese año.

`review_developer(desarrollador)` - Esta función toma como entrada una cadena de texto que representa el nombre de un desarrollador. Lee un archivo Parquet que contiene reseñas de los juegos de cada desarrollador. Filtra las reseñas para el desarrollador dado y luego devuelve un diccionario con la cantidad de reseñas positivas y negativas que ha recibido.

## Funcionalidad de la API con modelo de Machine Learning

<p align="center">
  <img src="images/image (6).jpg" width="400" alt="Texto alternativo si la imagen no carga">
</p>

- `recomend_user(usuario)` - 5 Recomendaciones para un usuario especifico, el modelo de machine learning entrenado con las bases de datos brindadas por la empresa le recomienda al usuario 5 juegos relacionados a su agrado en base a los juegos en los que dio su opinion, si el usuario no se encuentra en la base de datos o no dio valoraciones a ningun juego se le realizara una recomendacion aleatoria de juegos.

<h3><center>La forma en la que se creao y se utiliza cada funcion explicado con un enfoque tecnico, se encuentra detallada en profundidad en el directorio llamado FUNCIONES.</center></h3>

## Extract, Transform and Load (ETL)

A continuación, realizaré una breve referencia al trabajo que se realizó en cada uno de los conjuntos de datos. El concepto general es lograr que cada ETL y sus funciones sean reutilizables a medida que la base de datos principal continúa brindándonos información. Se trabajó con ese enfoque, asegurando que cada archivo sea reutilizable y se adapte al dataset original.

`games_preparado.csv.gz`: En este procedimiento, se extrajeron los datos de los juegos de la base de datos original de Steam. Los datos se limpiaron y transformaron para que solo contuvieran la información relevante para el análisis, como el título del juego, la fecha de lanzamiento, el desarrollador y el precio.
[limpieza_games.ipynb](ETL\limpiesa_games.ipynb)


`reviews_preparado.csv.gz`: Este conjunto de datos contiene las reseñas de los juegos de Steam. Se extrajeron las reseñas de la base de datos original, se limpiaron para eliminar cualquier dato innecesario o duplicado, y luego se transformaron para que solo contuvieran la información relevante para el análisis, como el ID del usuario, el ID del juego y la recomendación del usuario.
[limpieza_reviews.ipynb](ETL\limpiesa_reviews.ipynb)


`item_cantidad_usuarios.csv.gz`: Este dataset contiene información sobre la cantidad de juegos que tiene cada usuario. Se extrajo esta información de la base de datos original y se transformó en un formato fácil de analizar.
[limpieza_games.ipynb](ETL\limpiesa_games.ipynb)

`item_desplegado.csv.gz`: Este conjunto de datos contiene información detallada sobre cada juego que posee cada usuario. Se extrajo esta información de la base de datos original, se limpió para eliminar cualquier dato innecesario o duplicado, y luego se transformó para que solo contuviera la información relevante para el análisis. Además, se desanidó el total de los ítems que contiene cada usuario en su biblioteca.
[limpieza_games.ipynb](ETL\limpiesa_games.ipynb)

`Max_developer_year.csv`: Este conjunto de datos contiene información sobre qué desarrollador lanzó la mayor cantidad de juegos cada año. Se extrajo esta información de la base de datos original, se transformó para calcular la cantidad de juegos lanzados por cada desarrollador cada año, y luego se cargó en este documento.
[Funcion4.ipynb](Funciones\Funcion4.ipynb)

`recommends_dev.parquet`: Este conjunto de datos contiene las reseñas de los juegos de cada desarrollador. Se extrajeron las reseñas de la base de datos original, se transformaron para calcular la cantidad de reseñas positivas y negativas para cada desarrollador, y luego se cargaron en este conjunto de datos.
[Machine_learning.ipynb](Modelo\Machine_Learning.ipynb)


En cada caso, el resultado del proceso ETL es un documento que contiene datos limpios, transformados y listos para ser analizados. Cada conjunto de datos se puede cargar en un DataFrame para realizar análisis de datos.

Un detalle importante es que cada conjunto de datos se guardó y comprimió en los formatos más óptimos posibles. En la mayoría de los casos, elegí el tipo gzip debido a los bajos recursos de la plataforma para realizar el deploy. Este tipo de compresión no es el mejor en términos de almacenamiento, pero permite una rápida apertura además de requerir menos caudal de memoria.

Para los conjuntos de datos de mayor tamaño, realicé la lectura en base a chunks (o porciones). En la documentación dejé asentado en los momentos en que realicé la máxima optimización de los recursos. Estos procesos se llevaron a cabo para aprovechar al máximo los bajos recursos de la plataforma, priorizando la velocidad de respuesta al realizar cada consulta.


### Uso de la API

Accede a la API desplegada en [https://proyecto-steam-jac.onrender.com/].

Accede al entorno virtual de la API en [https://proyecto-steam-jac.onrender.com/docs].

## Autor

Nombre : Jonathan Ariel castillo

GitHub : [https://github.com/jonathancastillo185]

Linkedin : [https://www.linkedin.com/in/jonathan-castillo-7962b7163/]

 