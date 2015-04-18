from django.contrib import admin
from pagos.models import PagoPaypal
# Register your models here.


# Register your models here.



class PagoPaypalAdmin(admin.ModelAdmin):
    pass


admin.site.register(PagoPaypal, PagoPaypalAdmin)

