from fastapi import FastAPI, Body, Path,Query,Request,HTTPException,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from pydantic import BaseModel, Field
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
app.title = "Mi Aplicacion Sencilla"
app.version = "0.1.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, Request: Request):
        auth = await super().__call__(Request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=401, detail='invalid user')


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="nombre pelicula", min_length=2,max_length=50)
    overview: str = Field(default="descripcion pelicula", min_length=10,max_length=300)
    year :int = Field(default=2023 ,le=2023)
    rating :float = Field(default=10 ,ge=0 ,le=10)
    category : str = Field(default="comedia" ,min_length=4 ,max_length=15)


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Accion'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Accion'    
    } 
]

@app.get("/", tags=['home'])
def message ():
    return HTMLResponse(content="<h1> Mi APLICACION <h1>")

@app.get("/movies", tags=['movies'], response_model=list[Movie],status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get("/movies/{id}", tags=['movies'], status_code=200, response_model=Movie)
def get_movie(id : int) -> Movie :
    result=None
    for movie in movies:
        if movie['id']== id:
            result = movie
            break
    if result:
        return JSONResponse(content=result, status_code=200)
    else:
        return JSONResponse(content={"mensaje": "Movie not found"}, status_code=404)
        
@app.get("/movies/", tags=['movies'], status_code=200, response_model=list[Movie])
def get_movie_by_categoria(categoria : str) -> list[Movie]:
    result_category = []
    for movie in movies:
        if movie['category']== categoria:
            result_category.append(movie)
    if len(result_category)>0:
        return JSONResponse(content=result_category, status_code=200)
    else:
        return JSONResponse({"mensaje": "Movie not found"}, status_code=404)

        
        
@app.post("/movies", tags=['movies'], response_model=dict, status_code= 201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie.model_dump())
    return JSONResponse(content={"mensaje":"Movie created succesfully"},
                        status_code=201)

@app.put("/movies/{id}", tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie_data: Movie) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = movie_data.title
            movie['overview'] = movie_data.overview
            movie['year'] = movie_data.year
            movie['rating'] = movie_data.rating
            movie['category'] = movie_data.category
            break
    
    return JSONResponse(content={"message": "Movie Updated successfully"}, status_code=200)
 
@app.delete("/movies/{id}", tags=['movies'], response_model=dict, status_code=200 )
def delete_movie(id : int) -> dict:
    for movie in movies:
        if movie["id"]==id:
            movies.remove(movie)

    return JSONResponse({"mensaje":"Movie deleted successfully"})

class User(BaseModel):
    email:str
    password:str

# @app.post("/login", tags=['auth'], response_model=dict, status_code=200)
# def login(user : User) -> dict:
#     if user.email == "admin@gmail.com" and user.password == "admin":
#         token = create_token(data= user.model_dump())
#         return JSONResponse(content= {"token":token}, status_code=200)
#     else:
#         return JSONResponse(content={"mensaje": "invalid credencial"}, status_code=401)
@app.post("/login", tags=['auth'], response_model=dict, status_code=200)
def login(user : User) -> dict:
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(data= user.model_dump())
        return JSONResponse(content= {"token":token}, status_code=200)
    else:
        return JSONResponse(content={"mensaje": "invalid credencial"}, status_code=401)