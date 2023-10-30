# Proyecto Individual 1 - Sistema de Recomendación de Videojuegos para Steam

<p align="center">
  <img src="descarga.png" width="400" alt="Texto alternativo si la imagen no carga">
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

La API proporciona las siguientes funciones:

- `userdata(User_id)` - Detalles sobre el gasto del usuario, el porcentaje de recomendaciónes que realizo en base al total de items en su biblioteca, y la cantidad de items.

- `developer(desarrollador)` - Información sobre la cantidad de items y porcentaje de contenido gratuito por año según la empresa desarrolladora.

- `best_developer_year(año)` - Top 3 de desarrolladores con mas recomendaciones positivas por usuarios para un año específico.

- `review_developer(desarrollador)` - Cantidad de registros de reseñas de usuarios categorizados con análisis de sentimiento positivo o negativo según el desarrollador.

## Funcionalidad de la API con modelo de Machine Learning

<p align="center">
  <img src="image (6).jpg" width="400" alt="Texto alternativo si la imagen no carga">
</p>

- `recomend_user(usuario)` - 5 Recomendaciones para un usuario especifico, el modelo de machine learning entrenado con las bases de datos brindadas por la empresa le recomienda al usuario 5 juegos relacionados a su agrado en base a los juegos en los que dio su opinion, si el usuario no se encuentra en la base de datos o no dio valoraciones a ningun juego se le realizara una recomendacion aleatoria de juegos.

<h3><center>La forma en la que se creao y se utiliza cada funcion explicado con un enfoque tecnico, se encuentra detallada en profundidad en el directorio llamado FUNCIONES.</center></h3>


### Uso de la API

Accede a la API desplegada en [https://proyecto-steam-jac.onrender.com/].

Accede al entorno virtual de la API en [https://proyecto-steam-jac.onrender.com/docs].

## Autor

Nombre : Jonathan Ariel castillo

GitHub : [https://github.com/jonathancastillo185]

Linkedin : [https://www.linkedin.com/in/jonathan-castillo-7962b7163/]

 