from fastapi import FastAPI
import pandas as pd
import ast
import pyarrow.parquet as pq
import pickle
import json


app = FastAPI()

with open(r'Modelo/Machine.ipynb', 'rb') as file:
    model = pickle.load(file)

df = pd.read_csv(r'data_set_limpio/games_preparado.csv.gz')
opinion = pd.read_csv(r'data_set_limpio/reviews_preparado.csv.gz')
entrenar = pd.read_csv(r'data_set_limpio/modelo.csv.gz')
item_user = pd.read_csv(r'data_set_limpio/item_cantidad_usuarios.csv.gz')


@app.get('/userdata/{usuario}')
def userdata(user: str):
    try:
        if user not in item_user['user_id'].unique():
            return {f'El usuario {user}, no existe.'}
        usuario = 0
        chunks = pd.read_csv(r'data_set_limpio/item_desplegado.csv.gz', chunksize=200000)
        for chunk in chunks:
            if chunk['user'].isin([user]).any():
                usuario = chunk[chunk['user'] == user]
                break

        resultado = {
            'Usuario' : user,
            'Dinero gastado' : str(usuario['price'].sum())+'$',
            'cantidad de items' : str(item_user.loc[item_user['user_id'] == user]['items_count'].values[0]),
            'Porcentaje de recomendaciones' :str(round((len(opinion.loc[opinion['user'] == user])  / item_user.loc[item_user['user_id'] == user]['items_count'].values[0])*100,2))+'%'}
        
        return resultado
    except:
        return {'El usuario no se encuentra en la base de datos.'}



@app.get('/desarrollador/{developer}')
def developer(developer: str):
    if developer not in list(df['developer']):
        return {'El desarrollador no se encuentra en la base de datos'}

    fechas = df['release_date'].unique()

    anio = {}
    free = {}

    for x in fechas:
        filter_condition = (df['release_date'] == x) & (df['developer'] == developer)
        developer_releases = df[filter_condition]

        if len(developer_releases) != 0:
            anio[x] = len(developer_releases)
            free[x] = len(developer_releases[developer_releases['price'] == 0.0])

    for x, y in free.items():
        free[x] = f"{round((y / anio[x]) * 100, 2)}%"


    anio = {str(k): v for k, v in anio.items()}
    free = {str(k): v for k, v in free.items()}

    resultado = {'Cantidad de Items': anio, 'Contenido Free': free}

    return resultado



@app.get('/Top_3/{year}')
def best_developer_year(year : int):
    
        anio = pd.read_csv(r'data_set_limpio//Max_developer_year.csv')

            
        anio = anio.sort_values('Anio', ascending=False)
        
        seleccion = anio.loc[anio['Anio'] == year].copy()
        
        seleccion.fillna('Sin informacion',inplace=True)
        
        if not seleccion['Anio'].empty:
            respuesta = {'Anio': str(seleccion['Anio'].values[0]),
                        'Top 1': str(seleccion['Top 1'].values[0]),
                        'Top 2': str(seleccion['Top 2'].values[0]),
                        'Top 3': str(seleccion['Top 3'].values[0])
                        }
        else:
            respuesta = {f'No ingreso un valor relevante, este es el rango disponible ({str(anio["Anio"].min())} - {str(anio["Anio"].max())})'}

        return respuesta



@app.get('/Opiniones/{des}')
def review_developer( des : str ):
    
    try:

        table = pq.read_table(r'data_set_limpio/recomends_dev.parquet')
        
        dev = table.to_pandas()
        
        developer = dev.loc[dev['Developers'] == des]
        
        respuesta = {'Deloper' : str(developer['Developers'].values[0]), 'Reviews positivos' : str(developer['Positivo'].values[0]),'Reviews negativos' : str(developer['Negativo'].values[0])}
        dev = 0
        return respuesta
    
    except:
        
        return {'No ingreso un valor relevante, o el desarrollador no tiene Resenias' }  
    


@app.get('/Recomendaciones/{usuario}')
def recomend_user(usuario: str):
    if usuario not in entrenar['user'].unique():
        juegos_aleatorios = list(entrenar['app_name'].sample(5))
        mensaje = f'El usuario {usuario} no posee ningún item en su biblioteca, por lo que la recomendación será aleatoria.'
        return {mensaje: juegos_aleatorios}
    else:
        diccionario = {}
        
        juegos_valorados = entrenar[entrenar['user'] == usuario]['app_name'].unique()
        todos_los_juegos = entrenar['app_name'].unique()

        juegos_no_valorados = list(set(todos_los_juegos) - set(juegos_valorados))

        predicciones = [model.predict(usuario, juego) for juego in juegos_no_valorados]
        
        recomendaciones = sorted(predicciones, key=lambda x: x.est, reverse=True)[:5] 
        cont = 1
        for recomendacion in recomendaciones:
            diccionario[f'Top {cont}'] = recomendacion.iid
            cont += 1
        return {f'Usuario: {usuario}': diccionario}
    