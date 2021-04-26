from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from apps.codes.forms import CodeForm
from apps.userapp.models import CustomUser
from .utils import send_sms


@login_required
def home_view(request):
    return render(request,'core/frontpage.html', {})

def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.user
    if pk:
        user = request.user.customUser
        #user = CustomUser.objects.get(pk=pk)
        code = user.code
        code_user = f"{pk.username}: {user.code}"
        if request.method == 'GET':
            print(code_user)
            send_sms(code_user, user.contact) 
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()
                #login(request, user)
                return redirect('frontpage')
            else:
                messages.error(request, 'Wrong OTP')
                #return redirect('verify-view')
    return render(request, 'codes/verify.html', {'form':form})