'''
Created on 3 dic. 2018

@author: cami_
'''

import csv
from principal.models import *
import datetime
import os, django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SRecomendacion.settings')
django.setup()

users = pd.read_csv('data/user.txt', encoding = "latin1", sep='|', names=['userId','age','gender','occupation','zip_code'])
movies = pd.read_csv('data/item.txt',encoding = "latin1", sep='|',names=['movieId','title','release_date','vrelease_date','imdb_url', 'c_unknown','c_action','c_adventure','c_animation','c_children','c_comedy', 'c_crime','c_documentary','c_drama','c_fantasy','c_filmnoir','c_horror','c_musical','c_mystery','c_romance','c_scifi','c_thriller','c_war','c_western'])
ratings = pd.read_csv('data/data.txt',encoding = "latin1", sep=' ',names = ['userId','movieId','rating','date'])

def main():
#     for i, user in users.iterrows():
#         u = Usuario.objects.get_or_create(id=user['userId'], edad=user['age'], sexo=user['gender'], ocupacion=user['occupation'], codigo_postal=user['zip_code'])[0]
#     for i, movie in movies.iterrows():
#         categorias = []
#         if movie['c_unknown'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Unknown')[0]
#             categorias.append(c)
#         elif movie['c_action'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Action')[0]
#             categorias.append(c)
#         elif movie['c_adventure'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Adventure')[0]
#             categorias.append(c)
#         elif movie['c_animation'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Animation')[0]
#             categorias.append(c)
#         elif movie['c_children'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Children')[0]
#             categorias.append(c)
#         elif movie['c_comedy'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Comedy')[0]
#             categorias.append(c)
#         elif movie['c_crime'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Crime')[0]
#             categorias.append(c)
#         elif movie['c_documentary'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Documentary')[0]
#             categorias.append(c)
#         elif movie['c_drama'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Drama')[0]
#             categorias.append(c)
#         elif movie['c_fantasy'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Fantasy')[0]
#             categorias.append(c)
#         elif movie['c_filmnoir'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Filmnoir')[0]
#             categorias.append(c)
#         elif movie['c_horror'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Horror')[0]
#             categorias.append(c)
#         elif movie['c_musical'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Musical')[0]
#             categorias.append(c)
#         elif movie['c_mystery'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Mistery')[0]
#             categorias.append(c)
#         elif movie['c_romance'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Romance')[0]
#             categorias.append(c)
#         elif movie['c_scifi'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Scifi')[0]
#             categorias.append(c)
#         elif movie['c_thriller'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Thriller')[0]
#             categorias.append(c)
#         elif movie['c_war'] == 1:
#             c = Categoria.objects.get_or_create(nombre='War')[0]
#             categorias.append(c)
#         elif movie['c_western'] == 1:
#             c = Categoria.objects.get_or_create(nombre='Western')[0]
#             categorias.append(c)
#         
#         print(movie['release_date'])
#         print(movie['vrelease_date'])
#         r_date = None
#         vr_date = None
#         
#         if movie['release_date'] == movie['release_date']:
#             vr_date = datetime.datetime.strptime(movie['release_date'], '%d-%b-%Y').strftime('%Y-%m-%d')
#             
#         if movie['vrelease_date'] == movie['vrelease_date']:
#             vr_date = datetime.datetime.strptime(movie['vrelease_date'], '%d-%b-%Y').strftime('%Y-%m-%d')
#         
#         try:
#             pelicula = Pelicula.objects.get(id=movie['movieId'])
#         except:
#             pelicula = Pelicula(id=movie['movieId'],titulo=movie['title'],
#                 fecha_estreno=r_date, fecha_estreno_video=vr_date, imdb_url=movie['imdb_url'])
#             print(pelicula)
#             for c in categorias:
#                 pelicula.save()
#                 pelicula.categorias.add(Categoria.objects.get(nombre=c))
    for i, rating in ratings.iterrows():
        date = datetime.datetime.utcfromtimestamp(rating['date']).strftime('%Y-%m-%d') 
        user = Usuario.objects.get(id=rating['userId'])
        movie = Pelicula.objects.get(id=rating['movieId'])
        user_rating = Puntuacion(puntuacion=rating['rating'],fecha=date,usuario=user,pelicula=movie)
        user_rating.save()