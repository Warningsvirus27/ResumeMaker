from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Resume(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=timezone.now, editable=True)
    modification = models.DateTimeField(auto_now=timezone.now, editable=True, null=True, blank=True)

    def __str__(self):
        return str(self.user_id)


class Fields(models.Model):
    field_name = models.CharField(max_length=200, primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    has_date = models.BooleanField(default=False)
    sub_fields = models.ManyToManyField(Resume, through='SubField')

    def __str__(self):
        return str(self.field_name)


class SubField(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    field_id = models.ForeignKey(Fields, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.resume_id} for {self.field_id}"


class Document(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    doc_img = models.ImageField(upload_to='document_images')

    def __str__(self):
        return f"{self.user_id} for {self.name}"
