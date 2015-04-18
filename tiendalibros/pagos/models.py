from django.db import models
from decimal import Decimal

from libros.models import Libro

# Create your models here.

class PagoPaypalManager(models.Manager):
    def crear_pago(self, payment_id, libro):
        pago=self.create(libro=libro, 
            payment_id=payment_id, 
            precio=libro.precio)
        return pago
        


class PagoPaypal(models.Model):

    # Foreign Key hacia el libro de este pago
    libro = models.ForeignKey(Libro)
   
    # Identificador de paypal para este pago
    payment_id = models.CharField(max_length=64, db_index=True)

    # Id unico asignado por paypal a cada usuario no cambia aunque
    # la dirección de email lo haga.
    payer_id = models.CharField(max_length=128, blank=True, db_index=True)

    # Dirección de email del cliente proporcionada por paypal.
    payer_email = models.EmailField(blank=True)
    
    # Guardamos una copia del precio de libro, porque puede variar
    precio = models.DecimalField(max_digits=8, decimal_places=2,
            default = Decimal('0.00')) 

    pagado = models.BooleanField(default=False)

    creado = models.DateTimeField(auto_now_add=True, editable=False)
    
    objects = PagoPaypalManager()
