from project.models import *
from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(HawkerStall, Zipcode, History)
class ViewAdmin(ImportExportModelAdmin):
    pass