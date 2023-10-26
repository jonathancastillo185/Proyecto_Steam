from fastapi import FastAPI
import pandas as pd
import ast

app = FastAPI()


df = pd.read_csv(r'data_set_limpio/games_preparado.csv.gz')

item = pd.read_csv(r'data_set_limpio/items_preparado.csv.gz')

#opinion = pd.read_csv(r'data_set_limpio/reviews_preparado.csv.gz')



@app.get('/items/{developer}')
def developer(developer : str):
    
    fecha_inicio = df.loc[df['developer'] == developer]['release_date'].min()[:4]
    fecha_final =  df.loc[df['developer'] == developer]['release_date'].max()
    
    anio = {}
    free = {}
    
    while fecha_inicio <= fecha_final:
        if len(df[(df['release_date'] >= fecha_inicio) & (df['release_date'] <= fecha_inicio[:4]+'-12-31') & (df['developer'] == developer)]) > 0:
            anio[fecha_inicio[:4]] = len(df[(df['release_date'] >= fecha_inicio) & (df['release_date'] <= fecha_inicio[:4]+'-12-31') & (df['developer'] == developer)])
            free[fecha_inicio[:4]] = len(df[(df['release_date'] >= fecha_inicio) & (df['release_date'] <= fecha_inicio[:4]+'-12-31') & (df['developer'] == developer) & ((df['price'] == 'Free') | (df['price'] == 'Free to Play') )])
        fecha_inicio = str(int(fecha_inicio[:4])+1)+'-01-01'

    for x,y  in free.items():
        free[x] = str(round((y / anio[x])*100,2))+'%'
        
    resultado = {'Cantidad de Items': anio,'Contenido Free':free}
    
    return resultado






@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {'item_id' : item_id, 'q': q}



@app.get('/items/{developer}')
def mostrar(developer : str = NotImplemented):
    return df