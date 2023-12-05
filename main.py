from fastapi import FastAPI, Body
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
        
        
@app.post("/movies", tags=['movies'])
def create_movie(id: int = Body(),
                 title: str = Body(),
                 overvie: str = Body(),
                 year: str = Body(),
                 rating: float = Body(),
                 category : str = Body()):
    movies.append({
        'id':id,
        'title':title,
        'overvie':overvie,
        'year':year,
        'rating':rating,
        'category':category,
    })
    return movies

@app.put("/movies/{id}", tags=['movies'])
def uptade_movie(id: int = Body(),
                 title: str = Body(),
                 overvie: str = Body(),
                 year: str = Body(),
                 rating: float = Body(),
                 category : str = Body()):
    for movie in movie:
        if movie['id']== id :
            movie['title']= title
            movie['overview']= overvie
            movie['year']= year
            movie['rainting']= rating
            movie['category']= category
            break
    return movie
 
