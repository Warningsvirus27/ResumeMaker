from datetime import date
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
import base64
from qrcode import make
from qrcode.image import svg
import os


def year_list():
    years = []
    for index in range(80):
        years.append(date.today().year - index)
    return years


def get_resume_instance(request, resume):
    try:
        resume_instance = Resume.objects.get(id=resume)
    except Resume.DoesNotExist:
        messages.error(request, 'Invalid Resume ID')
        messages.error(request, 'Please try again !!!')
        return redirect('home')
    return resume_instance


def get_models_data(request, resume):
    content = {}
    if resume:
        resume_instance = get_resume_instance(request, resume)
    else:
        return 0

    try:
        personal_info_model = PersonalInformation.objects.get(resume=resume_instance)
        content['personal_info'] = personal_info_model
    except PersonalInformation.DoesNotExist:
        pass
    experience_model = Experience.objects.filter(resume=resume_instance)
    education_model = Education.objects.filter(resume=resume_instance)
    project_model = Project.objects.filter(resume=resume_instance)
    technical_skills_model = TechnicalSkills.objects.filter(resume=resume_instance)
    soft_skill_model = SoftSkills.objects.filter(resume=resume_instance)
    custom_field_model = CustomField.objects.filter(resume=resume_instance)
    if experience_model:
        content['experience'] = experience_model
    if education_model:
        content['education'] = education_model
    if project_model:
        content['project'] = project_model
    if technical_skills_model:
        content['tech_skills'] = technical_skills_model
    if soft_skill_model:
        content['soft_skills'] = soft_skill_model
    if custom_field_model:
        content['custom'] = custom_field_model

    return content


def get_models_tick(request, resume):
    content = {}
    if resume:
        resume_instance = get_resume_instance(request, resume)
    else:
        return 0

    try:
        PersonalInformation.objects.get(resume=resume_instance)
        content['personal_info_tick'] = 1
    except PersonalInformation.DoesNotExist:
        pass
    experience_model = Experience.objects.filter(resume=resume_instance)
    education_model = Education.objects.filter(resume=resume_instance)
    project_model = Project.objects.filter(resume=resume_instance)
    technical_skills_model = TechnicalSkills.objects.filter(resume=resume_instance)
    soft_skill_model = SoftSkills.objects.filter(resume=resume_instance)
    custom_field_model = CustomField.objects.filter(resume=resume_instance)
    if experience_model:
        content['experience_tick'] = 1
    if education_model:
        content['education_tick'] = 1
    if project_model:
        content['project_tick'] = 1
    if technical_skills_model:
        content['tech_skills_tick'] = 1
    if soft_skill_model:
        content['soft_skills_tick'] = 1
    if custom_field_model:
        content['custom_tick'] = 1

    return content


def get_rq_code_svg(link):
    link = str(base64.b64encode(link.encode('ascii')))[2:-1]
    img = make(link, image_factory=svg.SvgImage)
    img.save(f'resume/templates/images/qrcode/{link}.svg')
    return link + '.svg'
