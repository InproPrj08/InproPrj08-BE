import json
import traceback
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import View
from pass_portfolio.models import PassPortfolio
from recruit.models import Recruit
from .models import Portfolio, Comment, Interest, Status, College, Major
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import CommentForm, PortfolioForm


# Create your views here.
class PortfolioList(ListView):
    model = Portfolio
    template_name = 'portfolio_list.html'
    paginate_by = 6  # 페이지당 보여질 아이템 수
    page_kwarg = "page"

    def get_queryset(self):
        queryset = Portfolio.objects.all().order_by('-created_at')

        # 여기서부터 추가된 부분
        status = self.request.GET.get('status', '')
        interest = self.request.GET.get('interest', '')
        college = self.request.GET.get('college', '')
        major = self.request.GET.get('major', '')

        if status:
            queryset = queryset.filter(status1_id=True if status == 'True' else False)
        if interest:
            interest_obj = get_object_or_404(Interest, interest=interest)
            queryset = queryset.filter(interest_id=interest_obj.id)
        if college:
            queryset = queryset.filter(college=college)
        if major:
            major_obj = get_object_or_404(Major, slug=major)
            queryset = queryset.filter(major1_id=major_obj.id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 기존 코드와 다르게 수정
        status = self.request.GET.get('status', '')
        interest_name = self.request.GET.get('interest', '')
        college = self.request.GET.get('college', '')
        major_slug = self.request.GET.get('major1', '')

        # 관심 직무와 단과대를 불러오는 코드 추가
        interests = Interest.objects.all()
        colleges = College.objects.all()
        status = Status.objects.all()

        # 기존의 학과와 전공 정보
        sc = College.objects.get(name='과기')
        sm = Major.objects.filter(college=sc)
        pc = College.objects.get(name='약학')
        pm = Major.objects.filter(college=pc)
        ac = College.objects.get(name='아앤디')
        am = Major.objects.filter(college=ac)
        gc = College.objects.get(name='글융')
        gm = Major.objects.filter(college=gc)

        context.update({
            'status': status,
            'interest_name': interest_name,
            'college': college,
            'major_slug': major_slug,
            'majors': Major.objects.all(),  # 모든 전공을 가져오도록 수정
            'interests': interests,
            'colleges': colleges,
            'sm': sm,
            'pm': pm,
            'am': am,
            'gm': gm,
        })

        return context


class PortfolioDetail(DetailView):
    model = Portfolio
    template_name = 'portfolio/portfolio_detail.html'
    context_object_name = 'portfolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio = self.object  # 현재 포트폴리오 객체 사용

        context['comments'] = Comment.objects.filter(portfolio=portfolio).order_by('-created_at')
        context['form'] = CommentForm()


        # 특정 포트폴리오 객체를 사용하여 추가 데이터를 가져옵니다.
        if portfolio:
            interests = portfolio.interest_field.all()
            interest_names = [interest.interest for interest in interests]

            context['text_data'] = {
                'title': portfolio.title,
                'content': portfolio.content,
                'styles': portfolio.styles,
                'hashtags': json.loads(portfolio.hashtags) if portfolio.hashtags else [],
                'image': portfolio.image.url if portfolio.image else None,
                'interest_field': interest_names,
                'department': portfolio.department.name if portfolio.department else None,
                'status': portfolio.status,
                'status1':portfolio.anonymous,
            }
            print(portfolio.interest_field)
        else:
            context['text_data'] = None

        return context

    def post(self, request, pk):
        portfolio = get_object_or_404(Portfolio, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.portfolio = portfolio
            if request.user.is_authenticated:
                comment.user = request.user
                if comment.user == portfolio.author:  # 포트폴리오 작성자와 댓글 작성자가 동일한 경우
                    comment.is_portfolio_author = True  # Comment 모델에 is_portfolio_author 필드를 추가하여 구현
            else:
                comment.is_anonymous = True  # 예시 코드, 실제로 사용하려면 Comment 모델에 is_anonymous 필드를 추가해야 함

            comment.save()
            # 댓글을 작성한 후에 PortfolioDetail 페이지로 리디렉션
            return redirect('portfolio:portfolio_detail', pk=portfolio.pk)
        else:
            return self.form_invalid(form)


def search_view(request):
    query = request.GET.get('q')

    if query:
        # Portfolio, PassPortfolio, Recruit 각 모델에서 제목 또는 내용에 검색어가 포함된 경우를 찾습니다.
        portfolio_results = Portfolio.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        pass_portfolio_results = PassPortfolio.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        recruit_results = Recruit.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

        # 내용도 검색 결과에 포함시키기
        portfolio_results = portfolio_results.values('id', 'title', 'content')
        pass_portfolio_results = pass_portfolio_results.values('id', 'title', 'content')
        recruit_results = recruit_results.values('id', 'title', 'content')

        # 결과를 하나의 리스트로 합칩니다.
        results = list(chain(portfolio_results, pass_portfolio_results, recruit_results))
    else:
        # 검색어가 없는 경우 각 모델의 모든 객체를 가져옵니다.
        results = {
            'Portfolio': Portfolio.objects.all().values('id', 'title', 'content'),
            'PassPortfolio': PassPortfolio.objects.all().values('id', 'title', 'content'),
            'Recruit': Recruit.objects.all().values('id', 'title', 'content'),
        }

    return render(request, 'portfolio/search_results.html', {'results': results, 'query': query})



def your_combined_view(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portfolio:display_text')
    else:
        form = PortfolioForm()

    interests = Interest.objects.all()
    status = Status.objects.all()
    college = College.objects.all()
    sc = College.objects.get(name='과기')  # 선택한 학과 객체 가져오기
    sm = Major.objects.filter(college=sc)  # 해당 학과의 전공들 가져오기
    pc = College.objects.get(name='약학')  # 선택한 학과 객체 가져오기
    pm = Major.objects.filter(college=pc)  # 해당 학과의 전공들 가져오기
    ac = College.objects.get(name='아앤디')  # 선택한 학과 객체 가져오기
    am = Major.objects.filter(college=ac)  # 해당 학과의 전공들 가져오기
    gc = College.objects.get(name='글융')  # 선택한 학과 객체 가져오기
    gm = Major.objects.filter(college=gc)  # 해당 학과의 전공들 가져오기

    context = {
        'sm':sm,
        'pm':pm,
        'am': am,
        'gm': gm,
        'form': form,
        'interests': interests,
        'status': status,
        'college': college
    }

    return render(request, 'portfolio/index.html', context)


def save_text(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        print(form.data)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            styles = form.cleaned_data['styles']
            hashtags = form.cleaned_data['hashtags']
            image = form.cleaned_data['image']
            department = form.cleaned_data['department']
            status_value = form.cleaned_data['status']
            status = status_value
            print(status)
            status_value1 = form.cleaned_data['anonymous']
            status1 = status_value1
            print(status1)

            interest_field_ids = form.cleaned_data.get('interest_field')
            interest_instances = Interest.objects.filter(id__in=interest_field_ids)

            portfolio_instance = Portfolio(
                title=title,
                content=content,
                styles=styles,
                hashtags=hashtags,
                image=image,
                department=department,
                status=status,
                anonymous=status1,
                author=request.user
            )
            portfolio_instance.save()

            if interest_instances:
                portfolio_instance.interest_field.set(interest_instances)

            return JsonResponse({'status': 'success','pk': portfolio_instance.pk})
        else:
            print(form.errors)
            return JsonResponse({'status': 'error', 'message': '폼이 유효하지 않습니다.', 'errors': form.errors})
    else:
        return JsonResponse({'status': 'error', 'message': '잘못된 요청 방식입니다.'})


class PortfolioUpdate(UpdateView):
    model = Portfolio
    template_name = 'portfolio/portfolio_update.html'
    form_class = PortfolioForm

    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_college'] = self.object.department.college.name if self.object.department else 'default'
        context['selected_major'] = self.object.department.id if self.object.department else ''
        context['colleges'] = College.objects.all()
        context['interests'] = Interest.objects.all()
        context['sm'] = Major.objects.filter(college__name='과기')
        context['pm'] = Major.objects.filter(college__name='약학')
        context['am'] = Major.objects.filter(college__name='아앤디')
        context['gm'] = Major.objects.filter(college__name='글융')
        return context

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'pk': self.object.pk, 'is_ajax': True})
            else:
                return response
        except Exception as e:
            # 에러가 발생한 경우 로그에 출력
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': 'Internal Server Error'})


class PortfolioDeleteView(View):
    def post(self, request, pk):
        portfolio = get_object_or_404(Portfolio, pk=pk)

        # 권한 확인: 현재 사용자가 포트폴리오 작성자인지 확인
        if request.user == portfolio.author:
            portfolio.delete()
            response_data = {'status': 'success'}
        else:
            response_data = {'status': 'error', 'message': '포트폴리오 삭제 권한이 없습니다.'}

        return JsonResponse(response_data)

class DeleteCommentView(View):
    def post(self, request, pk, comment_id, *args, **kwargs):
        # 댓글을 삭제하는 뷰
        comment = get_object_or_404(Comment, pk=comment_id)

        # 권한 확인: 현재 사용자가 댓글 작성자인지 확인
        if request.user == comment.user:
            comment.delete()
            return redirect('portfolio:portfolio_detail', pk=pk)
        else:
            return JsonResponse({'status': 'error', 'message': 'No authority to delete'})


@login_required
def like(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if portfolio.like_users.filter(pk=request.user.pk):
        portfolio.like_users.remove(request.user)
        liked = False
    else:
        portfolio.like_users.add(request.user)
        liked = True

    like_count = portfolio.like_users.count()

    # JSON 응답 반환
    return JsonResponse({'liked': liked, 'like_count': like_count, 'status': 'success'})


@login_required
def toggle_comment_like(request, pk, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': comment.likes.count()})


def filter_portfolio_by_interest(interest_name):
    # QuerySet을 사용하여 필터링
    filtered_portfolios = Portfolio.objects.filter(
        interest_field__interest=interest_name
    )

    return filtered_portfolios


def filtersearch_view(request):
    majors = Major.objects.all()

    status_name = request.GET.get('status1')
    interest_names = request.GET.getlist('interest')
    college = request.GET.get('college')
    major = request.GET.get('major1')

    results = Portfolio.objects.all()

    if status_name:
        results = results.filter(status1_id=status_name == 'True')

    if interest_names:
        interest_filters = Q()
        for interest in interest_names:
            interest_filters |= Q(interest_field__interest=interest)
        results = results.filter(interest_filters)

    if college:
        results = results.filter(department__college__slug=college)

    if major:
        results = results.filter(department__slug=major)

    # 디버깅을 위해 쿼리 출력
    print(results.query)

    context = {
        'results': results,
        'majors': majors,
    }

    return render(request, 'portfolio/filtersearch_major_results.html', context)

def filter_page(request):
    majors = Major.objects.all()

    if request.method == 'GET':
        status = request.GET.get('status', '')
        interest = request.GET.getlist('interest')
        college = request.GET.get('college', '')
        major = request.GET.get('major', '')

        queryset = Portfolio.objects.all()

        if status:
            queryset = queryset.filter(status=status)

        if interest:
            # Update the filter for many-to-many relationship
            queryset = queryset.filter(interest_field__interest__in=interest)

        if college:
            queryset = queryset.filter(department__college=college)

        if major:
            queryset = queryset.filter(department=major)

        context = {
            'status': status,
            'interest': interest,
            'college': college,
            'major': major,
            'majors': majors,
            'results': queryset,
        }

        return render(request, 'portfolio/portfolio_list.html', context)


