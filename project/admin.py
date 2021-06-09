from project.models import HawkerStall, Zipcode
from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(HawkerStall, Zipcode)
class ViewAdmin(ImportExportModelAdmin):
    pass