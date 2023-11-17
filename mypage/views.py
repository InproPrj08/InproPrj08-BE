from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from portfolio.models import College, Major, Number, Portfolio
from portfolio.models import CUser as User
from .forms import UserForm
from django.core.paginator import Paginator

# Create your views here.
# 회원 가입
def main(request):
    return render(request, 'mypage/base.html')

def user_signup(request):
    Major.objects.all().order_by('name')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if request.POST['password'] == request.POST['confirm']:
            if form.is_valid():
                user = form.save(commit=False)
                user.password = request.POST['password']
                number = request.POST.get('number')
                user.number = Number.objects.get(number=number)
                college = request.POST.get('college')
                user.college = College.objects.get(name=college)
                if request.POST.get('major'):
                    major = request.POST.get('major')
                    user.major = Major.objects.get(name=major)
                user.save()
                login(request, user)
                return redirect("user:main")
    else:
        form = UserForm()
    return render(request, 'mypage/signup.html', {
        'form': form,
        'colleges': College.objects.all(),
        'majors': Major.objects.all().order_by('name'),
        'numbers': Number.objects.all().order_by('-number')
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.get(username=username)
        if user.password == password:
            login(request, user)
            print("인증성공")
            return redirect("user:main")  # 로그인 후 이동할 페이지 설정
        else:
            print("인증실패")
            return render(request, 'mypage/login.html', {'error': 'username or password is incorrect.'})
    return render(request, 'mypage/login.html')

#로그아웃
def user_logout(request):
    logout(request)
    return redirect("user:login")

def user_detail(request, username):
    user = User.objects.get(username=username)

    return render(request, 'mypage/my_detail.html',
                  {
                      'user':user
                  }
     )