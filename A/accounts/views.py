from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm, UserLoginForm, ChangePasswordForm, DateBirthForm, ProfileForm, \
    NumberPhoneForgetPassword
from .models import User
from random import randint
from .models import OtpCode
from utils import send_otp_code
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin



class RegisterView(View):
    form_class = UserRegisterForm
    templates_class = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_class, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = randint(10000, 99999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            cd = form.cleaned_data
            request.session['user_registered_info'] = {'phone_number': cd['phone_number'], 'password': cd['password_1']}
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')

        return render(request, self.templates_class, {'form': form})


class VerifyCodeRegisterView(View):
    form_class = VerifyCodeForm
    templates_class = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_class, {'form': form})

    def post(self, request):
        user_sessions = request.session['user_registered_info']
        code_instance = OtpCode.objects.get(phone_number=user_sessions['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == code_instance.code:
                User.objects.create_user(phone_number=user_sessions['phone_number'], password=user_sessions['password'])
                code_instance.delete()
                messages.success(request, 'OK Welcome ', 'success')
                return redirect('pages:home')
            else:
                messages.error(request, 'Not Math code', 'error')
                return redirect('accounts:verify_code')
        return render(request, self.templates_class, {'form': form})


class LoginView(View):
    form_class = UserLoginForm
    template_class = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_class, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('pages:home')
            messages.error(request, "Not Good Man", 'danger')
        return render(request, self.template_class, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "OK Good ", 'success')
        return redirect('pages:home')


class ProfileView(LoginRequiredMixin, View):
    template_class = 'accounts/profile.html'
    form_class = ProfileForm
    form_date = DateBirthForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_class, {'form': form, 'form_date': self.form_date})

    def post(self, request, ):
        form = self.form_class(request.POST)
        form_date = self.form_date(request.POST)
        if form.is_valid():

            if form_date.is_valid():
                date = form_date.cleaned_data
                cd = form.cleaned_data
                date_berth = f"{date['year']}/{date['mount']}/{date['day']}"
                request.user.profile.date_of_berth = date_berth
                request.user.profile.email = cd['email']
                request.user.profile.last_name = cd['last_name']
                request.user.profile.first_name = cd['first_name']
                request.user.profile.save()
                messages.success(request, 'پروفایل شما بروز رسانی شد', 'info')
                return redirect('accounts:profile')

            messages.success(request, 'پروفایل شما بروز رسانی نشد', 'danger')
            return redirect('accounts:profile')


class ChangePasswordView(LoginRequiredMixin, View):
    form_class = ChangePasswordForm
    template_name = 'accounts/change_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.set_password(form.cleaned_data['password_1'])
            user.save()
            messages.success(request, 'رمز شما با موفقیت تغییر یافت', 'success')
            return redirect('pages:home')
        messages.error(request, 'مشکلی پیش آمد لطفا دوباره تلاش کنید', 'danger')
        return redirect('accounts:change_password')


class ChangeProfile(LoginRequiredMixin, View):
    templates_class = 'accounts/change_profile.html'
    form_class = ProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile)
        return render(request, self.templates_class, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'OK', 'success')
            return redirect('accounts:profile')
        messages.error(request, 'NOT', 'warning')
        return redirect('accounts:change_profile')


class ChangeDateBirth(LoginRequiredMixin, View):
    templates_class = 'accounts/change_date_birth.html'
    form_class = DateBirthForm

    def get(self, request):
        return render(request, self.templates_class, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            day = cd['day']
            mount = cd['mount']
            year = cd['year']
            date = f'{year}/{mount}/{day}'
            request.user.profile.date_of_berth = date
            request.user.profile.save()
            messages.success(request, 'OK', 'success')
            return redirect('accounts:profile')
        messages.error(request, 'not good ', 'danger')
        return redirect('accounts:change_birth')


class ForgetPasswordView(View):
    form_class = NumberPhoneForgetPassword
    template_class = 'accounts/forget_password.html'

    def get(self, request):
        return render(request, self.template_class, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(phone_number=cd['number_phone'])
            if user:
                random_code = randint(10000, 99999)
                send_otp_code(cd['number_phone'], random_code)
                OtpCode.objects.create(phone_number=cd['number_phone'], code=random_code)
                request.session['user_forget_password'] = {'number_phone': cd['number_phone']}
                messages.success(request, 'we sent you a code', 'success')
                return redirect('accounts:verify_password')
            messages.success(request, 'کاربری پیدا نشد!!!', 'danger')
            return redirect('accounts:forget_password')
        messages.success(request, 'کاربری پیدا نشد!!!', 'danger')
        return redirect('accounts:forget_password')


class VerifyCodePasswordView(View):
    form_class = VerifyCodeForm
    template_class = 'accounts/verify_password.html'

    def get(self, request):
        return render(request, self.template_class, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            phone = request.session['user_forget_password']['number_phone']
            otp = OtpCode.objects.get(phone_number=phone)
            if not otp.active:
                messages.error(request, 'کد شما منقضی شده است!')
                return redirect('accounts:forget_password')
            if otp.code == code:
                return redirect('accounts:create_password')
        messages.error(request, "مشگلی پیش آمد دوباره تلاش کنید")
        return redirect('accounts:forget_password')


class CreateNewPasswordView(View):
    form_class = ChangePasswordForm
    template_class = 'accounts/create_password.html'

    def get(self, request):
        return render(request, self.template_class, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = request.session['user_forget_password']['number_phone']
            user = User.objects.get(user=phone)
            user.set_password(form.cleaned_data['password_1'])
            user.save()
            messages.success(request, 'رمز شما با موفقیت تغییر یافت', 'success')
            return redirect('accounts:login')
        messages.error(request, 'مشکلی پیش آمد دوباره تلاش کنید!', 'danger')
        return redirect('accounts:create_password')
