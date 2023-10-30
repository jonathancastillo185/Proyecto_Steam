from fastapi import FastAPI
import pandas as pd
import ast
import pyarrow.parquet as pq
import pickle



app = FastAPI()


with open('modelo_entrenado.pkl', 'rb') as file:
    model = pickle.load(file)

df = pd.read_csv(r'data_set_limpio/games_preparado.csv.gz')
opinion = pd.read_csv(r'data_set_limpio/reviews_preparado.csv.gz')
entrenar = pd.read_csv(r'data_set_limpio/modelo.csv.gz')



@app.get('/items_usuario/{usuario}')
def userdata(user: str):
    
    try:
        for x in pd.read_csv(r'data_set_limpio/items_preparado.csv.gz', chunksize=5000):
            if user in list(x['user_id']):
                aux = x
                break
            x = 0
                
        precios = []
        respuesta = {}
        
        
        usuario = aux.loc[aux['user_id'] == user]['items']
        
        
        if not usuario.empty:
            usuario = usuario.iloc[0]
        data = ast.literal_eval(usuario)
        result = pd.DataFrame(data)


        for y in result['item_name']:
            price = df.loc[df['app_name'] == y]['price'].values
            if len(price) > 0:
                try: 
                    price_value = float(price[0])
                    precios.append(price_value)
                except ValueError:
                    pass  
        
        respuesta['Usuario'] = user
        respuesta['Dinero gastado'] = str(round(sum(precios)))+' USD'
        respuesta["cantidad de items"] = str(len(result))
        
        respuesta['Porcentaje de recomendaciones'] = str(round(((len(opinion.loc[opinion['user'] == user]) / len(result))) * 100,2))+ '%'
        
        return respuesta
    except:
        return 'El usuario no se encuentra en la base de datos.'



@app.get('/desarrollador/{developer}')
def developer(developer : str):
    if developer not in list(df['developer']):
        return 'El desarrollador no se encuentra en la base de datos'
    

    fechas = df['release_date'].unique()
    
    anio = {}
    
    free = {}
    for x in fechas:
        if len(df[(df['release_date'] == x) & (df['developer'] == developer)]) != 0:
            anio[x] = len(df[(df['release_date'] == x) & (df['developer'] == developer)])
            free[x] = len(df[(df['release_date'] == x) & (df['developer'] == developer) & (df['price'] == 0.0)])
    for x,y  in free.items():
        free[x] = str(round((y / anio[x])*100,2))+'%'

    resultado = {'Cantidad de Items': anio,'Contenido Free':free}
    
    return resultado



@app.get('/Top_3/{year}')
def best_developer_year(year : int):
    
        anio = pd.read_csv('data_set_limpio//Max_developer_year.csv')

            
        anio = anio.sort_values('Anio', ascending=False)
        
        seleccion = anio.loc[anio['Anio'] == year].copy()
        
        seleccion.fillna('No existen resenias',inplace=True)
        
        
        
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
def resenias_developer( des : str ):
    
    try:

        table = pq.read_table('data_set_limpio/recomends_dev.parquet')
        
        dev = table.to_pandas()
        
        developer = dev.loc[dev['Developers'] == des]
        
        respuesta = {'Deloper' : str(developer['Developers'].values[0]), 'Reviews positivos' : str(developer['Positivo'].values[0]),'Reviews negativos' : str(developer['Negativo'].values[0])}
        dev = 0
        return respuesta
    
    except:
        
        return 'No ingreso un valor relevante, o el desarrollador no tiene Resenias'   
    



@app.get('/Recomendaciones/{usuario}')
def recomendaciones_usuario(usuario : str):
    
    if usuario not in entrenar['user'].unique():
        return {'El usuario no se encuentra en la base de datos'}
    else:
        diccionario = {}
        
        juegos_valorados = entrenar[entrenar['user'] == usuario]['app_name'].unique()

        todos_los_juegos = entrenar['app_name'].unique()

        juegos_no_valorados = list(set(todos_los_juegos) - set(juegos_valorados))

        predicciones = [model.predict(usuario, juego) for juego in juegos_no_valorados]
        
        recomendaciones = sorted(predicciones, key=lambda x: x.est, reverse=True)[:5] 
        cont = 1
        for recomendacion in recomendaciones:
            diccionario[f'Recomendacion - {cont}'] = recomendacion.iid
            cont+=1
        return diccionario
    
