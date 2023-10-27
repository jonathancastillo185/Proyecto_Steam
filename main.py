from fastapi import FastAPI
import pandas as pd
import ast


app = FastAPI()


df = pd.read_csv(r'data_set_limpio/games_preparado.csv.gz')

opinion = pd.read_csv(r'data_set_limpio/reviews_preparado.csv.gz')

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
        #result.dropna(inplace=True)
        #result.drop(columns='playtime_2weeks',inplace=True)


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



@app.get('/Top_3/{year}')
def best_developer_year(year : str):
    
    if isinstance(year, str):
        return {'Solo se admiten valores numericos'}
    elif isinstance(variable, int):
        year = int(year)
        
        anio = pd.read_csv(r'data_set_limpio/Max_developer_year.csv')
        
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



@app.get('/Recomendaciones/{des}')
def resenias_developer( des : str ):
    try:
        dev = pd.read_parquet(r'data_set_limpio/recomends_dev.parquet')
        
        developer = dev.loc[dev['Developers'] == des]
        
        respuesta = {'Deloper' : str(developer['Developers'].values[0]), 'Reviews positivos' : str(developer['Positivo'].values[0]),'Reviews negativos' : str(developer['Negativo'].values[0])}
        dev = 0
        return respuesta
    
    except:
        
        return 'No ingreso un valor relevante, o el desarrollador no se encuentra en la base de datos'