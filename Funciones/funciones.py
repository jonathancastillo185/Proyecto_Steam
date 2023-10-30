from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time



def extract(x): # ---> para desanidar los generos de games
    tags = []
    for x in x:
        tags.append(x)
    filtro = []
    for x in tags:
        for y in x.split(','):
            y = y.strip(" '[]'")
            filtro.append(y)
    return list(set(filtro))


    
def dumies_games(x): # ---> aca van los tags
    dicc = {}

    for x in list(x):
        dicc[x] = ''
        for y in df['tags']:
            if x in y:
                dicc[x] += '1'
            else:
                dicc[x] += '0'
    dicc1 = {}
    for x,e in dicc.items():
        dicc1[x] = [x for x in e]
        
    return pd.DataFrame(dicc1)
    
    
def extraer_anio(fecha): # --- > Esta funcion tiene la tarea de realizar una limpieza de los anios en la columna de release_date, returna solo el anio dejando de lado lo demas
    if '-' in fecha:  # Si el formato es 'YYYY-MM-DD'
        return fecha.split('-')[0]
    else:  # --- >  Si el formato es 'MMM YYYY'
        partes = fecha.split(' ')
        if len(partes) == 2:
            return partes[1]
    return fecha




def dumies_specs(x): # ---> aca van los tags
    dicc = {}

    for x in list(x):
        dicc[x] = ''
        for y in df['specs']:
            if x in y:
                dicc[x] += '1'
            else:
                dicc[x] += '0'
    dicc1 = {}
    for x,e in dicc.items():
        dicc1[x] = [x for x in e]
        
    return pd.DataFrame(dicc1)


def convertir_0(value): # --- > convertir todos los valores que no son float a 0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
    
    
'''

    Este archivo contiene todas las microfunciones que utilize para realizar los endpoints y los ETL correspondientes a los datasets que me brindaron

'''