from project.models import HawkerStall
from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(HawkerStall)
class ViewAdmin(ImportExportModelAdmin):
    pass