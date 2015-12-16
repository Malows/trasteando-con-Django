from django.db import models

# Create your models here.

class Ingrediente( models.Model ):
    nombre = models.CharField( max_length = 150 )

    def __str__(self):
        return self.nombre

class Pizza( models.Model ):
    nombre = models.CharField( max_length = 150 )
    precio = models.DecimalField ( decimal_places = 2 )
    ingredientes = models.ManyToManyField( Ingrediente )

    def __str__(self):
        return self.nombre
