from django.contrib import admin
from .models import*
# Register your models here.
admin.site.register(login)

admin.site.register(session)

admin.site.register(tbl_course)

# admin.site.register(tbl_student)

admin.site.register(tbll_student)

admin.site.register(tbl_payment)