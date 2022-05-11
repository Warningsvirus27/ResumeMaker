from django.contrib import admin
from .models import *


class ResumeAdmin(admin.ModelAdmin):
    search_fields = ['user_id_id']

    class Meta:
        model = Resume


class DocumentAdmin(admin.ModelAdmin):
    search_fields = ['user_id']

    class Meta:
        model = Resume


admin.site.register(Resume, ResumeAdmin)
admin.site.register(CustomField)
admin.site.register(PersonalInformation)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(TechnicalSkills)
admin.site.register(SoftSkills)
admin.site.register(Document, DocumentAdmin)
