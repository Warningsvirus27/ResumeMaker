from django.shortcuts import render, redirect
import base64
import smtplib
from email.message import EmailMessage
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import get_user_model
from .email_text import registration_text, password_text


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('howdoyoudothat27@gmail.com', '9527997644')
User = get_user_model()


def login(request):
    if request.method == 'POST':
        email = request.POST.get("email").strip().lower()
        checkbox = request.POST.get("forgot")

        if checkbox:
            return redirect(forgot_password, email, 1)

        password = request.POST.get("password")
        if not password:
            messages.error(request, 'Please input your password')
            return redirect('login')

        # user = auth.authenticate(request, email=email, password=password)
        try:
            user = User.objects.get(email=email)

            if user is not None:
                user = auth.authenticate(request, email=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Wrong Password!!')
                    messages.error(request, 'Please enter it again!!')
                    return redirect('login')
        except User.DoesNotExist as e:
            messages.error(request, 'User Does Not Exist!!')
            return render(request, 'html/login.html')
    else:
        return render(request, 'html/login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'html/logout.html')


def forgot_password(request, email, index):
    index = int(index)

    if index == 1:
        try:
            user = User.objects.get(email=email)
            encoded_email = str(base64.b64encode(email.encode('ascii')))[2:-1]
            link = f'{request.get_host()}/log/{encoded_email}/-1/forgot_password'
            text = password_text(user.first_name, user.last_name, link)

            msg = EmailMessage()
            msg.set_content(text)
            msg['Subject'] = "ResumeMaker Forgot Password"
            msg['From'] = "howdoyoudothat27@gmail.com"
            msg['To'] = email

            server.send_message(msg)
            messages.success(request, f'Email is successfully sent to {email}')
            messages.success(request, 'Click on it to Set Password')
            return redirect('login')
        except:
            messages.error(request, "Something went wrong please try again!!")
            messages.error(request, "We apologize for this inconvenience")
            return redirect('login')

    if index == -1:
        try:
            decoded_email = str(base64.b64decode(email))
        except:
            messages.error(request, "Invalid Web Url")
            messages.error(request, "Please proceed again!!")
            return redirect('login')
        return redirect(change_password, decoded_email[2:-1])


def change_password(request, email=None):
    if request.method == 'POST':
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        email_id = request.POST.get('email')

        if pass1 == pass2:
            try:
                user = User.objects.get(email=email_id)
                if user is not None:
                    user.set_password(pass1)
                    user.save()
                    messages.success(request, 'Password has been successfully changed')
                    messages.success(request, 'Please log in again!!')
                    return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User Doesnt exist for this link!!')
                return redirect('login')
        else:
            messages.error(request, 'Password Does not Match!!')
            return redirect(change_password, email_id)

    return render(request, 'html/forgot_password.html', {'email': email})


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('f_name').strip()
        last_name = request.POST.get('l_name').strip()
        email = request.POST.get('email').lower()

        try:
            user = User.objects.get(email=email)
            if user:
                messages.error(request, 'User Already Exists!!')
                return redirect('login')

        except User.DoesNotExist:
            encrypted_str = first_name+':'+last_name+','+email
            encrypted_str = str(base64.b64encode(encrypted_str.encode('ascii')))[2:-1]

            link = f'{request.get_host()}/log/{encrypted_str}/set_password'

            text = registration_text(first_name, last_name, link)

            # try:
            msg = EmailMessage()
            msg.set_content(text)
            msg['Subject'] = "ResumeMaker Registration"
            msg['From'] = "howdoyoudothat27@gmail.com"
            msg['To'] = email

            server.send_message(msg)
            messages.success(request, f'Email is successfully sent to {email}')
            messages.success(request, 'Click on it to Set Password')
            '''except:
                messages.error(request, 'Something went wrong please try again!')'''
    return render(request, 'html/register.html')


def set_password(request, user=None):
    return redirect(create_password, user=user)


def create_password(request, user=None):
    if request.method == 'GET':
        try:
            data = {}
            decrypted_str = str(base64.b64decode(user.split(',')[0]))[2:-1].split(',')
            name = decrypted_str[0].split(':')
            data['first_name'] = name[0]
            data['last_name'] = name[1]
            data['email'] = decrypted_str[1]

            return render(request, 'html/password.html', data)
        except:
            messages.error(request, 'Invalid URL')
            return redirect('login')

    if request.method == 'POST':
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        try:
            if pass1 == pass2:
                try:
                    user = User.objects.get(email=email)
                    if user is not None:
                        messages.error(request, 'User Already Exists!!')
                        return redirect('login')
                except User.DoesNotExist:
                    User.objects.create_user(email=email, password=pass1, first_name=first_name,
                                             last_name=last_name)
                    messages.success(request, 'User Successfully created!!')
                    messages.success(request, 'Kindly login again!')
                    return redirect('login')
            else:
                messages.error(request, 'Password Does not Match!!')
                return redirect(create_password, user=user)
        except:
            messages.error(request, "Something went wrong!")
            return render(request, 'html/login.html')
