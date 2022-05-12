from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from ckeditor.fields import RichTextField

User = get_user_model()
resume_choices = ((1, 'complete'),
                  (2, 'incomplete'))


class Resume(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=timezone.now, editable=True)
    modification = models.DateTimeField(editable=True, null=True, blank=True, default=None)
    status = models.CharField(max_length=20, choices=resume_choices)

    def __str__(self):
        return f'{self.user_id} {self.id}'


class CustomField(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    field_title = models.CharField(max_length=255)
    month = models.CharField(null=True, blank=True, max_length=255)
    year = models.IntegerField(null=True, blank=True)
    description = RichTextField()

    def __str__(self):
        return f"{self.resume_id} for {self.field_title}"


class PersonalInformation(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='profile_images')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    pin_code = models.IntegerField()
    country = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.BigIntegerField()
    summary = RichTextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    employer = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    month_start = models.CharField(max_length=255, blank=True, null=True)
    year_start = models.IntegerField(blank=True, null=True)
    month_end = models.CharField(max_length=255, blank=True, null=True)
    year_end = models.IntegerField(blank=True, null=True)
    job_description = models.TextField()

    def __str__(self):
        return f"{self.resume} for {self.job_title}"


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    study_field = models.CharField(max_length=255)
    graduation_month = models.CharField(max_length=255, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    percentage = models.CharField(max_length=20)
    suffix = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.resume} {self.degree}-{self.study_field}"


class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    month_start = models.CharField(max_length=255, blank=True, null=True)
    year_start = models.IntegerField(null=True, blank=True)
    month_end = models.CharField(max_length=255, blank=True, null=True)
    year_end = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.resume} {self.title}"


class TechnicalSkills(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=80)
    level = models.IntegerField()

    def __str__(self):
        return f"{self.resume} {self.skill_name}"


class SoftSkills(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=80)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.resume} {self.skill_name}"


class Document(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    doc_img = models.ImageField(upload_to='document_images')

    def __str__(self):
        return f"{self.user_id} for {self.name}"
