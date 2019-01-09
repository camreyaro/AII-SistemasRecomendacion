from django.shortcuts import render
import populate
from .forms import UsuarioForm, PeliculaForm
from .models import Usuario, Pelicula
from math import sqrt

# Create your views here.
def populate_db(request):
    populate.main()

def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

def sim_pearson(prefs, p1, p2):
  # Get the list of mutually rated items
  si = {}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item] = 1

  # if they are no ratings in common, return 0
  if len(si) == 0: return 0

  # Sum calculations
  n = len(si)
  
  # Sums of all the preferences
  sum1 = sum([prefs[p1][it] for it in si])
  sum2 = sum([prefs[p2][it] for it in si])
  
  # Sums of the squares
  sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
  sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])    
  
  # Sum of the products
  pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
  
  # Calculate r (Pearson score)
  num = pSum - (sum1 * sum2 / n)
  den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
  if den == 0: return 0

  r = num / den
  
  return r

def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]

  scores.sort()
  scores.reverse()
  return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_pearson):
  totals = {}
  simSums = {}
  for other in prefs:
    # don't compare me to myself
    if other == person: continue
    sim = similarity(prefs, person, other)

    # ignore scores of zero or lower
    if sim <= 0: continue
    for item in prefs[other]:
        
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item] == 0:
        # Similarity * Score
        totals.setdefault(item, 0)
        totals[item] += prefs[other][item] * sim
        # Sum of similarities
        simSums.setdefault(item, 0)
        simSums[item] += sim

  # Create the normalized list
  rankings = [(total / simSums[item], item) for item, total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings   

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result

def calculateSimilarItems(prefs,movie,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  scores={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  for item in itemPrefs:
    if item == movie.titulo:
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        break
  return scores

def recommended_movies(request):
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = Usuario.objects.get(id=form['usuario'].value())
            usuarios = Usuario.objects.all();
            dict = {}
            
            for u in usuarios:
                p_dict = {}
                for p in u.puntuacion_set.all():
                    p_dict[p.pelicula.titulo] = p.puntuacion
                    
                dict[u] = p_dict
            movies = getRecommendations(dict, user)
            return render(request, 'recomendaciones.html', {'movies': movies, 'form':form})

    else:
        form = UsuarioForm()

    return render(request, 'recomendaciones.html', {'form': form})

def similar_movies(request):
    
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            movie = Pelicula.objects.get(id=form['pelicula'].value())
            usuarios = Usuario.objects.all();
            dict = {}
            
            for u in usuarios:
                p_dict = {}
                for p in u.puntuacion_set.all():
                    p_dict[p.pelicula.titulo] = p.puntuacion
                dict[u] = p_dict
            movies = calculateSimilarItems(dict, movie, n=100)
            return render(request, 'similares.html', {'movie' : movie, 'movies': movies, 'form':form})

    else:
        form = PeliculaForm()

    return render(request, 'similares.html', {'form': form})
