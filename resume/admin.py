from django.contrib import admin
from .models import *


class ResumeAdmin(admin.ModelAdmin):
    search_fields = ['user_id_id']

    class Meta:
        model = Resume


class FieldsAdmin(admin.ModelAdmin):
    search_fields = ['field_name']

    class Meta:
        model = Resume


class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['user_id']

    class Meta:
        model = Resume


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Fields, FieldsAdmin)
admin.site.register(SubField)
admin.site.register(Document, DocumentAdmin)
