from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from portfolio.models import College, Major, Number, Portfolio, Interest, Status
from portfolio.models import CUser as User
from .forms import UserForm, CustomUserChangeForm
from django.core.paginator import Paginator

# Create your views here.
# 회원 가입
def main(request):
    return render(request, 'mypage/base.html')

def user_signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if request.POST['password'] == request.POST['confirm']:
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(request.POST['password'])
                number = request.POST.get('number')
                user.number = Number.objects.get(number=number)
                college = request.POST.get('college')
                user.college = College.objects.get(name=college)
                status = request.POST.get('status')
                user.status = Status.objects.get(status=status)

                # 다중 선택 필드 처리
                interest_interest = request.POST.getlist('interests')
                print("POST data:", request.POST)
                print("Interest values:", interest_interest)

                # user 객체를 먼저 저장하여 id 값이 할당되도록 합니다.
                user.save()

                # user.interests.set(...)을 호출할 때 id 값이 필요합니다.
                user.interests.set(Interest.objects.filter(id__in=interest_interest))
                print(user.interests.all())

                if request.POST.get('major'):
                    major = request.POST.get('major')
                    user.major = Major.objects.get(name=major)

                # user 객체를 최종적으로 저장합니다.
                user.save()

                login(request, user)
                return redirect("user:main")
            else:
                print("Form is not valid:", form.errors)
        else:
            print("Password and confirm password do not match.")
    else:
        form = UserForm()
    sc = College.objects.get(name='과기')  # 선택한 학과 객체 가져오기
    pc = College.objects.get(name='약학')  # 선택한 학과 객체 가져오기
    ac = College.objects.get(name='아앤디')  # 선택한 학과 객체 가져오기
    gc = College.objects.get(name='글융')  # 선택한 학과 객체 가져오기

    return render(request, 'mypage/signup.html', {
        'form': form,
        'colleges': College.objects.all(),
        'sm':Major.objects.filter(college=sc),
        'pm':Major.objects.filter(college=pc),
        'am':Major.objects.filter(college=ac),
        'gm':Major.objects.filter(college=gc),
        'numbers': Number.objects.all().order_by('-number'),
        'interests': Interest.objects.all(),
        'status': Status.objects.all(),

    })




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                print("인증 성공")
                return redirect("user:main")  # 로그인 후 이동할 페이지 설정
            else:
                print("인증 실패")
                return render(request, 'mypage/login.html', {'form': form, 'error': '유효하지 않은 사용자명 또는 비밀번호입니다.'})
        else:
            print("폼 유효성 검사 실패")
            return render(request, 'mypage/login.html', {'form': form, 'error': '잘못된 폼 제출입니다.'})
    else:
        form = AuthenticationForm()

    return render(request, 'mypage/login.html', {'form': form})

#로그아웃
def user_logout(request):
    logout(request)
    return redirect("user:login")

# def user_detail(request, username):
#     user = User.objects.get(username=username)
#
#     return render(request, 'mypage/my_detail.html',
#                   {
#                       'user': user
#                   }
#      )
def user_detail(request, username):
    user = User.objects.get(username=username)

    # Reverse 사용 예시
    detail_url = reverse('user:detail', args=[username])

    return render(request, 'mypage/my_detail.html', {'user': user, 'detail_url': detail_url})

#내가 작성한 글 보기
def user_portfolios(request, username):
    user_portfolios = Portfolio.objects.filter(author__username=username)
    context = {'user_portfolios': user_portfolios}
    return render(request, 'mypage/user_portfolios.html', context)

def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profileImage'):
        profile_image = request.FILES['profileImage']

        # 이미지를 저장할 경로 설정 (예시: media 폴더)
        save_path = 'media/profile_images/' + profile_image.name

        with open(save_path, 'wb') as destination:
            for chunk in profile_image.chunks():
                destination.write(chunk)

        # 업로드 성공 시 이미지 URL 반환
        return JsonResponse({'status': 'success', 'imageUrl': '/' + save_path})

    # 업로드 실패 시
    return JsonResponse({'status': 'fail'})


@login_required
def user_update(request, username):  # 이 부분 수정
    user = get_object_or_404(get_user_model(), username=username)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, '회원 정보가 성공적으로 수정되었습니다.')
            return redirect('user:user_detail', username=user.username)  # 이 부분 수정
        else:
            messages.error(request, '유효하지 않은 입력이 있습니다. 다시 시도해주세요.')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'mypage/update.html', {'form': form})