from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from .helper import *


def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'html/homepage.html')
    else:
        return HttpResponse('Invalid entry')


def template_edit(request, template_id=None):
    user = request.user
    data = {'mail': user.get_username(), 'name': user.get_full_name()}

    return render(request, 'html/srt-resume.html', data)


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
    content = {'email': request.user, 'resume': resume_id, 'year': year_list()}
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
                resume_instance = get_resume_instance(request, resume_id)
                content['experiences'] = Experience.objects.filter(resume=resume_instance)
                if len(content['experiences']) == 0:
                    content['count'] = 1
                else:
                    content['count'] = len(content['experiences']) + 1
                content.update(get_models_tick(request, resume_id))

                return render(request, 'html/create_resume_experience.html', content)

            elif field == "education":
                resume_instance = get_resume_instance(request, resume_id)
                content['educations'] = Education.objects.filter(resume=resume_instance)
                if len(content['educations']) == 0:
                    content['count'] = 1
                else:
                    content['count'] = len(content['educations']) + 1
                content.update(get_models_tick(request, resume_id))

                return render(request, 'html/create_resume_education.html', content)

            elif field == "projects":
                resume_instance = get_resume_instance(request, resume_id)
                content['projects'] = Project.objects.filter(resume=resume_instance)
                if len(content['projects']) == 0:
                    content['count'] = 1
                else:
                    content['count'] = len(content['projects']) + 1
                content.update(get_models_tick(request, resume_id))

                return render(request, 'html/create_resume_projects.html', content)

            elif field == "technical_skills":
                content['counter'] = [1, 2, 3]
                resume_instance = get_resume_instance(request, resume_id)
                content['tech_skills'] = TechnicalSkills.objects.filter(resume=resume_instance)
                if len(content['tech_skills']) == 0:
                    content['count'] = 1
                else:
                    content['count'] = len(content['tech_skills']) + 1
                content.update(get_models_tick(request, resume_id))

                return render(request, 'html/create_resume_technical_skills.html', content)

            elif field == "soft_skills":
                content['counter'] = [1, 2, 3]
                resume_instance = get_resume_instance(request, resume_id)
                content['soft_skills'] = SoftSkills.objects.filter(resume=resume_instance)
                if len(content['soft_skills']) == 0:
                    content['count'] = 1
                else:
                    content['count'] = len(content['soft_skills']) + 1
                content.update(get_models_tick(request, resume_id))

                return render(request, 'html/create_resume_soft_skills.html', content)

            elif field == "custom":
                resume_instance = get_resume_instance(request, resume_id)
                content['custom_fields'] = CustomField.objects.filter(resume=resume_instance)
                if len(content['custom_fields']) == 0:
                    content['count'] = 1
                else:
                    content['count'] = len(content['custom_fields']) + 1
                content.update(get_models_tick(request, resume_id))
            elif field == 'view_template':
                content.update(get_models_tick(request, resume_id))

                return render(request, 'html/template_html.html', content)

            return render(request, 'html/create_resume_custom.html', content)

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
            elif field == "projects":
                redirect_field = get_projects(request, resume_id)
                return redirect(create_resume, resume_id, redirect_field)
            elif field == "technical_skills":
                redirect_field = get_technical_skills(request, resume_id)
                return redirect(create_resume, resume_id, redirect_field)
            elif field == "soft_skills":
                redirect_field = get_soft_skills(request, resume_id)
                return redirect(create_resume, resume_id, redirect_field)
            elif field == "custom":
                redirect_field = get_custom(request, resume_id)
                if redirect_field == 'view_template':
                    return redirect('view_template', resume_id)
                return redirect(create_resume, resume_id, redirect_field)
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
        img_available = request.POST.get('img_available')

        resume_instance = get_resume_instance(request, resume)

        try:
            personal_info_model = PersonalInformation.objects.get(resume=resume_instance)
            if not image and img_available:
                pass
            else:
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

        if month_start and year_start and month_end and year_end:
            pass
        elif month_start or year_start or month_end or year_end:
            messages.error(request, "please input all Start Date-Year and Ending Date-Year")
            messages.error(request, "Single input will not be considered!!")
            return 'experience'
        else:
            month_start, year_start, month_end, year_end = None, None, None, None

        resume_instance = get_resume_instance(request, resume)

        try:
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
        except Experience.DoesNotExist:
            experience_model = Experience(resume=resume_instance, employer=employer, job_title=job_title,
                                          city=city, state=state, month_start=month_start,
                                          year_start=year_start, month_end=month_end,
                                          year_end=year_end, job_description=job_description)
            experience_model.save()

        if add_new or delete:
            return 'experience'
        else:
            return 'education'


def get_education(request, resume):
    if request.method == "POST":
        school_name = request.POST.get('school_name').strip().capitalize()
        city = request.POST.get('city').strip().capitalize()
        state = request.POST.get('state').strip().capitalize()
        if request.POST.get('custom_degree'):
            degree = request.POST.get('custom_degree')
        else:
            degree = request.POST.get('degree')
        study_field = request.POST.get('study_field').strip().capitalize()
        graduation_month = request.POST.get('month')
        if graduation_month == "None":
            graduation_month = None
        graduation_year = request.POST.get('year')
        if graduation_year == "None":
            graduation_year = None
        percentage = request.POST.get('percentage')
        if request.POST.get('custom_percentage'):
            suffix = request.POST.get('custom_percentage')
        else:
            suffix = request.POST.get('suffix')
        presently_working = request.POST.get('present')
        education_instance = request.POST.get('current')
        add_new = request.POST.get('add_new')
        delete = request.POST.get('delete')

        if not degree:
            messages.error(request, "Please Input degree")
            return 'education'

        if presently_working:
            graduation_month = None
            graduation_year = None

        if graduation_month and graduation_year:
            pass
        elif graduation_month or graduation_year:
            messages.error(request, "please input both Month and Year")
            messages.error(request, "Single input will not be considered!!")
            return 'experience'
        else:
            graduation_month, graduation_year = None, None

        resume_instance = get_resume_instance(request, resume)
        try:
            education_model = Education.objects.get(id=education_instance)
            if delete:
                education_model.delete()
            else:
                education_model.school_name = school_name
                education_model.city = city
                education_model.state = state
                education_model.degree = degree
                education_model.study_field = study_field
                education_model.graduation_month = graduation_month
                education_model.graduation_year = graduation_year
                education_model.percentage = percentage
                education_model.suffix = suffix
                education_model.save()
        except Education.DoesNotExist:
            education_model = Education(resume=resume_instance, school_name=school_name, city=city,
                                        state=state, degree=degree, study_field=study_field,
                                        graduation_year=graduation_year, graduation_month=graduation_month,
                                        percentage=percentage, suffix=suffix)
            education_model.save()

        if add_new or delete:
            return 'education'
        else:
            return 'projects'


def get_projects(request, resume):
    if request.method == "POST":
        title = request.POST.get('title').strip().capitalize()
        month_start = request.POST.get('month_start')
        year_start = request.POST.get('year_start')
        month_end = request.POST.get('month_end')
        year_end = request.POST.get('year_end')
        description = request.POST.get('description').strip()
        presently_working = request.POST.get('present')
        project_instance = request.POST.get('current')
        add_new = request.POST.get('add_new')
        delete = request.POST.get('delete')

        if presently_working:
            month_end = None
            year_end = None

        if month_start and year_start and month_end and year_end:
            pass
        elif month_start or year_start or month_end or year_end:
            messages.error(request, "please input All Start Date-Year and Ending Date-Year")
            messages.error(request, "Single input will not be considered!!")
            return 'experience'
        else:
            month_start, year_start, month_end, year_end = None, None, None, None

        resume_instance = get_resume_instance(request, resume)

        try:
            project_model = Project.objects.get(id=project_instance)
            if delete:
                project_model.delete()
            else:
                project_model.title = title
                project_model.month_start = month_start
                project_model.year_start = year_start
                project_model.month_end = month_end
                project_model.year_end = year_end
                project_model.description = description
                project_model.save()
        except Project.DoesNotExist:
            project_model = Project(resume=resume_instance, title=title, month_start=month_start,
                                    year_start=year_start, month_end=month_end, year_end=year_end,
                                    description=description)
            project_model.save()

        if add_new or delete:
            return 'projects'
        else:
            return 'technical_skills'


def get_technical_skills(request, resume):
    if request.method == "POST":
        skill_name = request.POST.get('name').strip().capitalize()
        level = request.POST.get('level')
        project_instance = request.POST.get('current')
        add_new = request.POST.get('add_new')
        delete = request.POST.get('delete')
        new = request.POST.get('new')
        if new:
            data_dict = {'inp1': [request.POST.get('name1'), request.POST.get('level1')],
                         'inp2': [request.POST.get('name2'), request.POST.get('level2')],
                         'inp3': [request.POST.get('name3'), request.POST.get('level3')],
                         }

        resume_instance = get_resume_instance(request, resume)

        try:
            technical_skills_model = TechnicalSkills.objects.get(id=project_instance)
            if delete:
                technical_skills_model.delete()
            else:
                technical_skills_model.skill_name = skill_name
                technical_skills_model.level = level
                technical_skills_model.save()
        except TechnicalSkills.DoesNotExist:
            if new:
                for key, value in data_dict.items():
                    if value[0]:
                        technical_skills_model = TechnicalSkills(resume=resume_instance, skill_name=value[0], level=value[1])
                        technical_skills_model.save()
            else:
                technical_skills_model = TechnicalSkills(resume=resume_instance, skill_name=skill_name, level=level)
                technical_skills_model.save()

        if add_new or delete:
            return 'technical_skills'
        else:
            return 'soft_skills'


def get_soft_skills(request, resume):
    if request.method == "POST":
        skill_name = request.POST.get('name').strip().capitalize()
        description = request.POST.get('description').strip().capitalize()
        project_instance = request.POST.get('current')
        add_new = request.POST.get('add_new')
        delete = request.POST.get('delete')
        new = request.POST.get('new')
        if new:
            data_dict = {'inp1': [request.POST.get('name1'), request.POST.get('description1')],
                         'inp2': [request.POST.get('name2'), request.POST.get('description2')],
                         'inp3': [request.POST.get('name3'), request.POST.get('description3')],
                         }

        resume_instance = get_resume_instance(request, resume)

        try:
            soft_skills_model = SoftSkills.objects.get(id=project_instance)
            if delete:
                soft_skills_model.delete()
            else:
                soft_skills_model.skill_name = skill_name
                soft_skills_model.description = description
                soft_skills_model.save()
        except SoftSkills.DoesNotExist:
            if new:
                for key, value in data_dict.items():
                    if value[0]:
                        soft_skills_model = SoftSkills(resume=resume_instance, skill_name=value[0],
                                                       description=value[1])
                        soft_skills_model.save()
            else:
                soft_skills_model = SoftSkills(resume=resume_instance, skill_name=skill_name,
                                               description=description)
                soft_skills_model.save()

        if add_new or delete:
            return 'soft_skills'
        else:
            return 'custom'


def get_custom(request, resume):
    if request.method == "POST":
        field = request.POST.get('field').strip().capitalize()
        header = request.POST.get('header').strip().capitalize()
        month = request.POST.get('month')
        year = request.POST.get('year')
        description = request.POST.get('description').strip().capitalize()
        project_instance = request.POST.get('current')
        add_new = request.POST.get('add_new')
        delete = request.POST.get('delete')

        resume_instance = get_resume_instance(request, resume)

        try:
            custom_field_model = CustomField.objects.get(id=project_instance)
            if delete:
                custom_field_model.delete()
            else:
                custom_field_model.field_title = field
                custom_field_model.header = header
                custom_field_model.description = description
                custom_field_model.month = month
                custom_field_model.year = year
                custom_field_model.save()
        except CustomField.DoesNotExist:
            custom_field_model = CustomField(resume=resume_instance, field_title=field, header=header,
                                             description=description, month=month, year=year)
            custom_field_model.save()

        if add_new or delete:
            return 'custom'
        else:
            return 'view_template'


def template(request, resume=None):
    content = get_models_data(request, resume)
    content['qr_code'] = get_rq_code_svg(request.user.get_username())
    return render(request, 'resume/html/first_temp.html', content)


def document_check(request, requester=None, user=None):
    if requester and user:
        pass
    else:
        messages.error(request, 'Something went wrong Please try again!!')
        return redirect('home')
