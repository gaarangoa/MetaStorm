from django.contrib import admin
from .models import Job, Fastqfile, Reference
# Register your models here.

class JobDisplay(admin.ModelAdmin):
    list_display = ('arc_id', 'date', 'sid', 'pid', 'pip', 'status')
    list_filter = ('pip', 'status')
    search_fields = ('sid', 'pid', 'sid')

admin.site.register(Job, JobDisplay)
admin.site.register(Fastqfile)
admin.site.register(Reference)