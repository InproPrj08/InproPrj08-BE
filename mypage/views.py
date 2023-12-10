import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from portfolio.models import College, Major, Number, Portfolio, Interest, Status
from portfolio.models import CUser as User
from recruit.models import Recruit
from pass_portfolio.models import PassPortfolio
from .forms import UserForm
from django.core.paginator import Paginator


# Create your views here.

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
                return redirect(reverse('user:detail', args=[user.username]))
            else:
                print("Form is not valid:", form.errors)
        else:
            print("Password and confirm password do not match.")
    else:
        form = UserForm()

    sc = College.objects.get(name='과학기술대학')  # 선택한 학과 객체 가져오기
    pc = College.objects.get(name='약학대학')  # 선택한 학과 객체 가져오기
    ac = College.objects.get(name='아트앤디자인대학')  # 선택한 학과 객체 가져오기
    gc = College.objects.get(name='글로벌융합대학')  # 선택한 학과 객체 가져오기

    return render(request, 'mypage/signup.html', {
        'form': form,
        'colleges': College.objects.all(),
        'sm': Major.objects.filter(college=sc),
        'pm': Major.objects.filter(college=pc),
        'am': Major.objects.filter(college=ac),
        'gm': Major.objects.filter(college=gc),
        'numbers': Number.objects.all().order_by('-number'),
        'interests': Interest.objects.all(),
        'status': Status.objects.all(),
    })


@csrf_protect
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
                return redirect(reverse('user:detail', args=[user.username]))  # 로그인 후 이동할 페이지 설정
            else:
                print("인증 실패")
                return render(request, 'mypage/login.html', {'form': form, 'error': '유효하지 않은 사용자명 또는 비밀번호입니다.'})
        else:
            print("폼 유효성 검사 실패")
            return render(request, 'mypage/login.html', {'form': form, 'error': '잘못된 폼 제출입니다.'})
    else:
        form = AuthenticationForm()

    return render(request, 'mypage/login.html', {'form': form})


# 로그아웃
def user_logout(request):
    logout(request)
    return redirect("user:login")


def user_detail(request, username):
    user = User.objects.get(username=username)

    detail_url = reverse('user:detail', args=[username])
    user_recruit = Recruit.objects.filter(author__username=username)

    return render(request, 'mypage/my_detail.html',
                  {'user': user, 'detail_url': detail_url, 'user_recruit': user_recruit})


# 내가 작성한 포트폴리오 글 보기
def user_portfolios(request, username):
    context = {}  # Initialize the context dictionary

    # Assuming you have a User model for the author field
    user_portfolios = Portfolio.objects.filter(author__username=username)

    if user_portfolios.exists():
        # Assuming you have a ForeignKey field named interest_field in the Portfolio model
        interests = user_portfolios[0].interest_field.all()

        # Retrieve the interest names from the related Interest model
        interest_names = [interest.interest for interest in interests]

        context['text_data'] = {
            'pk': user_portfolios[0].pk,
            'title': user_portfolios[0].title,
            'content': user_portfolios[0].content,
            'styles': user_portfolios[0].styles,
            'hashtags': json.loads(user_portfolios[0].hashtags) if user_portfolios[0].hashtags else [],
            'image': user_portfolios[0].image.url if user_portfolios[0].image else None,
            'interest_field': interest_names,
            'department': user_portfolios[0].department.name if user_portfolios[0].department else None,
            'status': user_portfolios[0].status,
            'status1': user_portfolios[0].anonymous,
            'author': user_portfolios[0].author,
            'created_at': user_portfolios[0].created_at,

            'interests': Interest.objects.all(),  # 추가: 관심 직무 모델에서 모든 값 가져오기
            'colleges': College.objects.all(),  # 추가: 단과대 모델에서 모든 값 가져오기
            'statuss': Status.objects.all(),  # 추가: 상태 모델에서 모든 값 가져오기
        }
        print("Status:", user_portfolios[0].status)
        print("Interests:", user_portfolios[0].interest_field.all())

    return render(request, 'mypage/user_portfolios.html', context)


# 내가 작성한 합격 수기 글 보기
# 내가 작성한 글 보기
def user_pass_portfolios(request, username):
    context = {}  # Initialize the context dictionary

    # Assuming you have a User model for the author field
    user_pass_portfolios = PassPortfolio.objects.filter(author__username=username)

    if user_pass_portfolios.exists():
        # Assuming you have a ForeignKey field named interest_field in the Portfolio model
        interests = user_pass_portfolios[0].interest_field.all()

        # Retrieve the interest names from the related Interest model
        interest_names = [interest.interest for interest in interests]

        context['text_data'] = {
            'pk': user_pass_portfolios[0].pk,
            'title': user_pass_portfolios[0].title,
            'content': user_pass_portfolios[0].content,
            'styles': user_pass_portfolios[0].styles,
            'hashtags': json.loads(user_pass_portfolios[0].hashtags) if user_pass_portfolios[0].hashtags else [],
            'image': user_pass_portfolios[0].image.url if user_pass_portfolios[0].image else None,
            'interest_field': interest_names,
            'department': user_pass_portfolios[0].department.name if user_pass_portfolios[0].department else None,
            'status1': user_pass_portfolios[0].anonymous,
            'author': user_pass_portfolios[0].author,
            'company_name': user_pass_portfolios[0].company_name,
            'created_at': user_pass_portfolios[0].created_at,

            'interests': Interest.objects.all(),  # 추가: 관심 직무 모델에서 모든 값 가져오기
            'colleges': College.objects.all(),  # 추가: 단과대 모델에서 모든 값 가져오기
        }
        print("Interests:", user_pass_portfolios[0].interest_field.all())

    return render(request, 'mypage/user_pass_portfolios.html', context)


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


def user_update(request, username):
    user = get_object_or_404(get_user_model(), username=username)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # 기존 회원 정보를 업데이트
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

            # 유저 이름 업데이트
            new_username = request.POST.get('username')
            user.username = new_username
            user.save()

            login(request, user)
            return redirect("user:detail", username=user.username)
        else:
            print("Form is not valid:", form.errors)
    else:
        # 기존 회원 정보를 폼에 전달하여 초기값으로 설정
        form = UserForm(initial={
            'number': user.number.number,
            'college': user.college.name,
            'status': user.status.status,
            'major': user.major.name if user.major else '',
            'interests': user.interests.all(),
            # 여기에 다른 필드 추가 가능
        })

    sc = College.objects.get(name='과학기술대학')
    pc = College.objects.get(name='약학대학')
    ac = College.objects.get(name='아트앤디자인대학')
    gc = College.objects.get(name='글로벌융합대학')

    return render(request, 'mypage/update.html', {
        'form': form,
        'user': user,  # 추가: 유저 정보를 템플릿으로 전달
        'colleges': College.objects.all(),
        'sm': Major.objects.filter(college=sc),
        'pm': Major.objects.filter(college=pc),
        'am': Major.objects.filter(college=ac),
        'gm': Major.objects.filter(college=gc),
        'numbers': Number.objects.all().order_by('-number'),
        'interests': Interest.objects.all(),
        'status': Status.objects.all(),
    })
