from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi Aplicacion Sencilla"
app.version = "0.1.1"

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accion'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accion'    
    } 
]

@app.get("/", tags=['home'])
def message ():
    return HTMLResponse(content="<h1> Mi APLICACION <h1>")

@app.get("/movies", tags=['movies'])
def get_movies():
    return movies

@app.get("/movies/{id}", tags=['movies'])
def get_movie(id : int):
    for movie in movies:
        if movie['id']== id:
            return movie
        
@app.get("/movies/", tags=['movies'])
def get_movie_by_categoria(categoria : str ,):
    for movie in movies:
        if movie['category']== categoria:
            return movie
        
@app.get("/movies/", tags=['movies'])
def get_movie_by_title(titulo : str ):
    for movie in movies:
        if movie['title']== titulo:
            return movie