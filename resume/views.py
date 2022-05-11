from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth import get_user_model
from .models import *
from django.contrib import messages
from datetime import date


def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'html/homepage.html')
    else:
        return HttpResponse('Invalid entry')


def template_edit(request, template_id=None):
    user = request.user
    data = {'mail': user.get_username(), 'name': user.get_full_name()}

    return render(request, 'html/srt-resume.html', data)


def get_resume_instance(request, resume):
    try:
        resume_instance = Resume.objects.get(id=resume)
    except Resume.DoesNotExist:
        messages.error(request, 'Invalid Resume ID')
        messages.error(request, 'Please try again !!!')
        return redirect('home')
    return resume_instance


def create_new_resume(request):
    if request.user.is_authenticated:
        UserModel = get_user_model()
        try:
            current_user = UserModel.objects.get(email=request.user)
        except UserModel.DoesNotExist:
            messages.error(request, f'User with {request.user} does not exist or may have been deleted')
            messages.error(request, 'We are sorry for the inconvenience')
            return render(request, 'html/error_page.html')

        resume_instance = Resume(user_id=current_user, creation_date=timezone.now(), status='incomplete')
        resume_instance.save()
        return redirect(create_resume, resume_instance.id, 'personal_info')
    else:
        return render(request, 'html/error_page.html')


def create_resume(request, resume_id=None, field=None):
    content = {'email': request.user, 'resume': resume_id}
    if request.user.is_authenticated:
        if request.method == "GET":

            if field == "personal_info" or field is None:
                resume_instance = get_resume_instance(request, resume_id)
                try:
                    content['personal_info'] = PersonalInformation.objects.get(resume=resume_instance)
                except PersonalInformation.DoesNotExist:
                    pass
                return render(request, 'html/create_resume_personal_info.html', context=content)

            elif field == "experience":
                year_list = []
                for index in range(80):
                    year_list.append(date.today().year - index)
                content['year'] = year_list

                resume_instance = get_resume_instance(request, resume_id)
                try:
                    PersonalInformation.objects.get(resume=resume_instance)
                    content['personal_info_tick'] = 1
                    content['resume'] = resume_id
                    content['experiences'] = Experience.objects.filter(resume=resume_instance)
                    if len(content['experiences']) == 0:
                        content['count'] = 1
                    else:
                        content['count'] = len(content['experiences']) + 1
                except PersonalInformation.DoesNotExist:
                    pass

                return render(request, 'html/create_resume_experience.html', content)

            elif field == "education":
                return render(request, 'html/create_resume_education.html', content)
            elif field == "skills":
                return render(request, 'html/create_resume_skills.html', content)
            elif field == "summary":
                return render(request, 'html/create_resume_summary.html', content)
            elif field == "review":
                return render(request, 'html/create_resume_review.html', content)

        if request.method == "POST":
            if field == "personal_info":
                get_personal_info(request, resume_id)
                return redirect(create_resume, resume_id=resume_id, field='experience')
            elif field == "experience":
                redirect_field = get_experience(request, resume_id)
                return redirect(create_resume, resume_id, redirect_field)
            elif field == "education":
                redirect_field = get_education(request, resume_id)
                return redirect(create_resume, resume_id, redirect_field)
            elif field == "skills":
                get_skills(request, template_id)
            elif field == "summary":
                get_summary(request, template_id)
            elif field == "review":
                get_review(request, template_id)
    else:
        return render(request, 'html/error_page.html')


def get_personal_info(request, resume):
    if request.method == "POST":
        address = request.POST.get('address')
        try:
            address = ', '.join(list(map(lambda s: s.capitalize(), address.strip().split(','))))
        except AttributeError:
            pass

        first_name = request.POST.get('first_name').strip().capitalize()
        last_name = request.POST.get('last_name').strip().capitalize()
        address = address
        city = request.POST.get('city').strip().capitalize()
        pin_code = int(request.POST.get('pin_code'))
        country = request.POST.get('country').strip().capitalize()
        email = request.POST.get('email').strip()
        phone_number = int(request.POST.get('phone_number'))
        image = request.FILES.get('image')
        summary = request.POST.get('summary').strip()

        resume_instance = get_resume_instance(request, resume)

        try:
            personal_info_model = PersonalInformation.objects.get(resume=resume_instance)
            personal_info_model.image = image
            personal_info_model.first_name = first_name
            personal_info_model.last_name = last_name
            personal_info_model.address = address
            personal_info_model.city = city
            personal_info_model.pin_code = pin_code
            personal_info_model.country = country
            personal_info_model.email = email
            personal_info_model.phone_number = phone_number
            personal_info_model.summary = summary
            personal_info_model.save()
        except PersonalInformation.DoesNotExist:
            personal_info_model = PersonalInformation(resume=resume_instance, first_name=first_name,
                                                      last_name=last_name, address=address, city=city,
                                                      pin_code=pin_code, country=country, email=email,
                                                      phone_number=phone_number, image=image,
                                                      summary=summary)
            personal_info_model.save()
        return


def get_experience(request, resume):
    if request.method == "POST":
        employer = request.POST.get('employer').strip().capitalize()
        job_title = request.POST.get('job_title').strip()
        city = request.POST.get('city').strip().capitalize()
        state = request.POST.get('state').strip().capitalize()
        month_start = request.POST.get('month_start')
        year_start = request.POST.get('year_start')
        month_end = request.POST.get('month_end')
        year_end = request.POST.get('year_end')
        job_description = request.POST.get('job_description').strip()
        presently_working = request.POST.get('present')
        experience_instance = request.POST.get('current')
        add_new = request.POST.get('add_new')
        delete = request.POST.get('delete')

        if presently_working:
            current_date = date.today()
            month_end = current_date.strftime('%B')
            year_end = current_date.year

        resume_instance = get_resume_instance(request, resume)
        print('this is delete', delete)
        try:
            print('try started')
            experience_model = Experience.objects.get(id=experience_instance)
            if delete:
                experience_model.delete()
            else:
                experience_model.employer = employer
                experience_model.job_title = job_title
                experience_model.city = city
                experience_model.state = state
                experience_model.month_start = month_start
                experience_model.year_start = year_start
                experience_model.month_end = month_end
                experience_model.year_end = year_end
                experience_model.job_description = job_description
                experience_model.save()
            print('try ended')
        except Experience.DoesNotExist:
            print('exception raised')
            experience_model = Experience(resume=resume_instance, employer=employer, job_title=job_title,
                                          city=city, state=state, month_start=month_start,
                                          year_start=year_start, month_end=month_end,
                                          year_end=year_end, job_description=job_description)
            experience_model.save()
            print('exception ended')
        if add_new or delete:
            return 'experience'
        else:
            return 'education'


def get_education(request, resume):
    if request.method == "POST":
        employer = request.POST.get('employer').strip().capitalize()
        job_title = request.POST.get('job_title').strip()
        city = request.POST.get('city').strip().capitalize()
        state = request.POST.get('state').strip().capitalize()
        month_start = request.POST.get('month_start')
        year_start = request.POST.get('year_start')
        month_end = request.POST.get('month_end')
        year_end = request.POST.get('year_end')
        job_description = request.POST.get('job_description').strip()
        presently_working = request.POST.get('present')
        experience_instance = request.POST.get('current')
        add_new = request.POST.get('add_new')
        delete = request.POST.get('delete')

        if presently_working:
            current_date = date.today()
            month_end = current_date.strftime('%B')
            year_end = current_date.year

        resume_instance = get_resume_instance(request, resume)
        print('this is delete', delete)
        try:
            print('try started')
            experience_model = Experience.objects.get(id=experience_instance)
            if delete:
                experience_model.delete()
            else:
                experience_model.employer = employer
                experience_model.job_title = job_title
                experience_model.city = city
                experience_model.state = state
                experience_model.month_start = month_start
                experience_model.year_start = year_start
                experience_model.month_end = month_end
                experience_model.year_end = year_end
                experience_model.job_description = job_description
                experience_model.save()
            print('try ended')
        except Experience.DoesNotExist:
            print('exception raised')
            experience_model = Experience(resume=resume_instance, employer=employer, job_title=job_title,
                                          city=city, state=state, month_start=month_start,
                                          year_start=year_start, month_end=month_end,
                                          year_end=year_end, job_description=job_description)
            experience_model.save()
            print('exception ended')
        if add_new or delete:
            return 'experience'
        else:
            return 'education'


def get_skills(request, template_id): pass
def get_summary(request, template_id): pass
def get_review(request, template_id): pass
