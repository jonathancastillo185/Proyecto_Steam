from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    print(input('excribe un numero'))