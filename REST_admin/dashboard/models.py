# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    user_id = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "admin"


class Aligner(models.Model):
    aligner_id = models.TextField(unique=True)  # This field type is a guess.
    aligner_name = models.TextField(unique=True)  # This field type is a guess.
    aligner_default = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    aligner_fast = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    aligner_sensitive = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "aligner"


class Assembler(models.Model):
    assembler_id = models.TextField(unique=True)  # This field type is a guess.
    assembler_name = models.TextField(unique=True)  # This field type is a guess.
    assembler_default = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    assembler_fast = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    assembler_sensitive = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "assembler"


class Assembly(models.Model):
    sample_id = models.TextField()  # This field type is a guess.
    user_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    project_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    datasets = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "assembly"


class Fastqfile(models.Model):
    id = models.TextField(unique=True, blank=True, null=False, primary_key=True)
    pid = models.TextField(blank=True, null=True)
    file = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "fastqFiles"


class Files(models.Model):
    project_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    file = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "files"


class Job(models.Model):
    uid = models.TextField(blank=True, null=True)
    pid = models.TextField(blank=True, null=True)
    sid = models.TextField(blank=True, null=True)
    pip = models.TextField(blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    priority = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    arc_id = models.TextField(blank=True, null=False, primary_key=True)

    class Meta:
        managed = True
        db_table = "jobs"
        unique_together = (("arc_id"),)

    def __unicode__(self):
        return self.arc_id


class Matches(models.Model):
    sample_id = models.TextField()  # This field type is a guess.
    user_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    project_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    datasets = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "matches"


class NumberJobs(models.Model):
    priority = models.TextField(unique=True, blank=True, null=True)
    jobs = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "number_jobs"


class Project(models.Model):
    project_id = models.TextField(
        unique=True, primary_key=True
    )  # This field type is a guess.
    project_name = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    project_short_description = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    project_description = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    project_path = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "project"


class ProjectStatus(models.Model):
    user_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    project_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    sample_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    pipeline = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "project_status"


class ProjectStatusReads(models.Model):
    user_id = models.TextField(blank=True, null=True)
    project_id = models.TextField(blank=True, null=True)
    sample_id = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    pipeline = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "project_status_reads"


class QualityFilter(models.Model):
    sid = models.TextField(unique=True, blank=True, null=True)
    num_reads = models.IntegerField(blank=True, null=True)
    qc_reads = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "quality_filter"


class Reference(models.Model):
    reference_id = models.TextField(
        unique=True, primary_key=True
    )  # This field type is a guess.
    reference_name = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    sequence_type = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    reference_description = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    reference_path = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    user_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    seqfile = models.TextField(blank=True, null=True)  # This field type is a guess.
    taxofile = models.TextField(blank=True, null=True)  # This field type is a guess.
    functfile = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    reference_format_path = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reference"


class SampleRun(models.Model):
    sample_id = models.TextField(blank=True, null=True)
    process = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "sample_run"


class SampleStatus(models.Model):
    id = models.TextField(unique=True, blank=True, null=False, primary_key=True)
    sid = models.TextField(blank=True, null=True)
    rid = models.TextField(blank=True, null=True)
    pip = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sample_status"


class Samples(models.Model):
    sample_id = models.TextField(unique=True)  # This field type is a guess.
    project_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    sample_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    sample_set = models.TextField(blank=True, null=True)  # This field type is a guess.
    environment = models.TextField(blank=True, null=True)  # This field type is a guess.
    library_preparation = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    reads1 = models.TextField(blank=True, null=True)  # This field type is a guess.
    reads2 = models.TextField(blank=True, null=True)  # This field type is a guess.
    lat = models.TextField(blank=True, null=True)
    lng = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "samples"


class Session(models.Model):
    uid = models.TextField()
    ip = models.TextField()
    browser = models.TextField()
    status = models.TextField()

    class Meta:
        managed = False
        db_table = "session"
        unique_together = (("uid", "ip", "browser"),)


class User(models.Model):
    user_id = models.TextField()  # This field type is a guess.
    user_password = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    user_name = models.TextField()  # This field type is a guess.
    user_affiliation = models.TextField(unique=True)  # This field type is a guess.
    organization = models.TextField()
    country = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "user"


class UserProjects(models.Model):
    user_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    project_id = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "user_projects"


class Version(models.Model):
    version_id = models.TextField(unique=True)  # This field type is a guess.
    metagenome_id = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    aligner_id = models.TextField(blank=True, null=True)  # This field type is a guess.
    aligner_parameters = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    assembler_id = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    assembler_parameters = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.
    reference_id = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.

    class Meta:
        managed = False
        db_table = "version"

