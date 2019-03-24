from django.contrib import admin
from .models import Job, Fastqfile, Reference, SampleStatus, Project

# Register your models here.


class JobDisplay(admin.ModelAdmin):
    list_display = ("arc_id", "date", "sid", "pid", "pip", "status")
    list_filter = ("pip", "status")
    search_fields = ("sid", "pid", "sid")


class ReferenceDisplay(admin.ModelAdmin):
    list_display = (
        "reference_id",
        "user_id",
        "reference_name",
        "sequence_type",
        "reference_description",
        "seqfile",
        "status",
        "reference_format_path",
    )
    list_filter = ("user_id", "status", "sequence_type")
    search_fields = ("reference_name", "user_id")


class SampleStatusDisplay(admin.ModelAdmin):
    list_display = ("id", "sid", "rid", "pip", "status")
    list_filter = ("pip", "status")
    search_fields = ("sid", "rid")


class FastqfileDisplay(admin.ModelAdmin):
    list_display = ("id", "pid", "file", "status")
    # list_filter = ("id", "pid")
    search_fields = ("id", "pid")


class ProjectDisplay(admin.ModelAdmin):
    list_display = ("project_id", "project_name", "project_description")
    # list_filter = ("project_name", "project_id")
    search_fields = ("project_id", "project_name")


admin.site.register(Job, JobDisplay)
admin.site.register(Fastqfile, FastqfileDisplay)
admin.site.register(Reference, ReferenceDisplay)
admin.site.register(SampleStatus, SampleStatusDisplay)
admin.site.register(Project, ProjectDisplay)
