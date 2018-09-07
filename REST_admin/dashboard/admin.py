from django.contrib import admin
from .models import Job, Fastqfile, Reference, SampleStatus
# Register your models here.


class JobDisplay(admin.ModelAdmin):
    list_display = ('arc_id', 'date', 'sid', 'pid', 'pip', 'status')
    list_filter = ('pip', 'status')
    search_fields = ('sid', 'pid', 'sid')


class ReferenceDisplay(admin.ModelAdmin):
    list_display = ('reference_id', 'user_id', 'reference_name', 'sequence_type',
                    'reference_description', 'seqfile', 'status', 'reference_format_path')
    list_filter = ('user_id', 'status', 'sequence_type')
    search_fields = ('reference_name', 'user_id')


class SampleStatusDisplay(admin.ModelAdmin):
    list_display = ('id', 'sid', 'rid', 'pip','status')
    list_filter = ('sid', 'pip', 'status')
    search_fields = ('sid', )

admin.site.register(Job, JobDisplay)
admin.site.register(Fastqfile)
admin.site.register(Reference, ReferenceDisplay)
admin.site.register(SampleStatus, SampleStatusDisplay)
