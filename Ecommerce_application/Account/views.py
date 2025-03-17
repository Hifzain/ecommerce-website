from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password, make_password
from Account.models import userData
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes  # Use force_text here
from django.views import View
import re
from django.utils.http import urlsafe_base64_decode




def SignUp(request):
    if request.method == 'POST':
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        phone = request.POST.get('phoneno', '').strip()
        email = request.POST.get('email', '').strip()
        pwd = request.POST.get('password', '').strip()

        if not all([fname, lname, phone, email, pwd]):
            messages.error(request, "All fields are required!")
            return redirect('savedata')

        if userData.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('savedata')

        try:
            user = userData(
                first_name=fname,
                last_name=lname,
                Phone=phone,
                email=email,
                password=make_password(pwd)  # Hash the password before saving
            )
            user.save()

            messages.success(request, "Account created successfully!")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
            return redirect('savedata')

    return render(request, 'Register.html')



def user_loginPage(request):
    if request.method == "POST":
        login_email = request.POST.get('email', '').strip()
        login_password = request.POST.get('password', '').strip()

        if not login_email or not login_password:
            return render(request, 'Login.html')

        try:
            user = userData.objects.get(email=login_email)

            if check_password(login_password, user.password):  # Check hashed password
                request.session['user_id'] = user.id
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")

        except userData.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, 'Login.html')




def logout(request):
    if request.session.has_key('user_id'):
        del request.session['user_id']
        messages.success(request, "Logout successfully")
        return redirect('home')
        # return render(request,'home.html', {'logoutsuccess': True})
    else: 
        return redirect('login')


class PasswordResetRequestView(View):
    def get(self, request):
        return render(request, 'password_reset.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = userData.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))

            # Construct the reset URL
            reset_url = f"{request.scheme}://{request.get_host()}/reset-password-confirm/{uid}/{token}/"

            # Send email
            send_mail(
                'Password Reset Request',
                f'Hi {user.first_name},\n\nClick the link below to reset your password:\n{reset_url}',
                'DEFAULT_FROM_EMAIL',  
                [user.email],
                fail_silently=False,
            )
            return render(request, 'password_reset_done.html')
        except userData.DoesNotExist:
            return render(request, 'password_reset.html', {'error': 'Email not found'})

# Password Reset Confirm View
class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})

    def post(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))  # Updated here
            user = userData.objects.get(pk=uid)  # Ensure correct user model
            token_generator = PasswordResetTokenGenerator()
            
            if token_generator.check_token(user, token):
                new_password = request.POST.get('new_password')

                # Validate password length and complexity
                if len(new_password) < 6 or not re.search(r'\d', new_password) or not re.search(r'[A-Za-z]', new_password):
                    messages.error(request, 'Password must be at least 6 characters long and contain both letters and numbers.')
                    return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})

                user.set_password(new_password)
                user.save()
                return redirect('login')  # Redirect to a success page after reset

            # If the token is invalid
            return render(request, 'password_reset_confirm.html', {'error': 'Invalid token or the link has expired'})

        except userData.DoesNotExist:
            # If user does not exist
            return render(request, 'password_reset_confirm.html', {'error': 'Invalid token or user does not exist'})



from django.contrib.auth.hashers import make_password
