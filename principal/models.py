from django.db import models

# Create your models here.
class Usuario(models.Model):
    sex = (
    ("M", "M"),
    ("F", "F"),)
    id = models.IntegerField(primary_key=True)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=100, choices=sex)
    ocupacion = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.id) + " " + str(self.edad) + " " + self.ocupacion

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
     
class Pelicula(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    fecha_estreno = models.DateField(null=True)
    fecha_estreno_video = models.DateField(null=True)
    imdb_url= models.CharField(max_length=100)
    categorias = models.ManyToManyField(Categoria)
    puntuaciones = models.ManyToManyField(Usuario, through='Puntuacion')
    
    def __str__(self):
        return self.titulo
    
class Puntuacion(models.Model):
    puntuacion = models.IntegerField()
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.puntuacion)