import json
import traceback

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from portfolio.models import Interest, Status, College, Major
from .forms import PassCommentForm, PassPortfolioForm
from .models import PassPortfolio, PassComment
from django.views.generic import ListView, DetailView, UpdateView, DeleteView



# Create your views here.
class PassPortfolioList(ListView):
    model = PassPortfolio
    template_name = 'pass_portfolio/pass_portfolio_list.html'
    context_object_name = 'pass_portfolio'
    paginate_by = 6  # 페이지당 보여질 아이템 수
    page_kwarg = "page"
    def get_queryset(self):
        return PassPortfolio.objects.all().order_by('-created_at')


class PassPortfolioDetail(DetailView):
    model = PassPortfolio
    template_name = 'pass_portfolio/pass_portfolio_detail.html'
    context_object_name = 'pass_portfolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pass_portfolio = self.object  # 현재 포트폴리오 객체 사용

        context['comments'] = PassComment.objects.filter(pass_portfolio=pass_portfolio).order_by('-created_at')
        context['form'] = PassCommentForm()

        # 특정 포트폴리오 객체를 사용하여 추가 데이터를 가져옵니다.
        if pass_portfolio:
            interests = pass_portfolio.interest_field.all()
            interest_names = [interest.interest for interest in interests]

            context['text_data'] = {
                'title': pass_portfolio.title,
                'content': pass_portfolio.content,
                'styles': pass_portfolio.styles,
                'hashtags': json.loads(pass_portfolio.hashtags) if pass_portfolio.hashtags else [],
                'image': pass_portfolio.image.url if pass_portfolio.image else None,
                'interest_field': interest_names,
                'department': pass_portfolio.department.name if pass_portfolio.department else None,
                'company_name': pass_portfolio.company_name,
                'company_info':pass_portfolio.company_info,
            }
            print(pass_portfolio.interest_field)
        else:
            context['text_data'] = None

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PassCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pass_portfolio = self.object
            comment.user = self.request.user  # Assuming user is authenticated
            comment.is_anonymous = request.POST.get('is_anonymous') == 'on'
            comment.save()
            # 댓글을 작성한 후에 PortfolioDetail 페이지로 리디렉션
            return redirect('pass_portfolio:pass_portfolio_detail', pk=self.object.pk)
        else:
            return self.form_invalid(form)


@login_required
def like(request, pk):
    pass_portfolio = get_object_or_404(PassPortfolio, pk=pk)
    if pass_portfolio.like_users.filter(pk=request.user.pk):
        pass_portfolio.like_users.remove(request.user)
        liked = False
    else:
        pass_portfolio.like_users.add(request.user)
        liked = True

    like_count = pass_portfolio.like_users.count()

    # JSON 응답 반환
    return JsonResponse({'liked': liked, 'like_count': like_count, 'status': 'success'})


def your_combined_view(request):
    if request.method == 'POST':
        form = PassPortfolioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_text/')
    else:
        form = PassPortfolioForm()

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

    return render(request, 'pass_portfolio/index.html', context)


def save_text(request):
    if request.method == 'POST':
        form = PassPortfolioForm(request.POST, request.FILES)
        print(form.data)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            styles = form.cleaned_data['styles']
            hashtags = form.cleaned_data['hashtags']
            image = form.cleaned_data['image']
            department = form.cleaned_data['department']
            company_name = form.cleaned_data['company_name']
            company_info = form.cleaned_data['company_info']

            interest_field_ids = form.cleaned_data.get('interest_field')
            interest_instances = Interest.objects.filter(id__in=interest_field_ids)

            pass_portfolio_instance = PassPortfolio(
                title=title,
                content=content,
                styles=styles,
                hashtags=hashtags,
                image=image,
                department=department,
                company_info=company_info,
                company_name=company_name,
                author=request.user
            )
            pass_portfolio_instance.save()

            if interest_instances:
                pass_portfolio_instance.interest_field.set(interest_instances)

            return JsonResponse({'status': 'success','pk': pass_portfolio_instance.pk})
        else:
            print(form.errors)
            return JsonResponse({'status': 'error', 'message': '폼이 유효하지 않습니다.', 'errors': form.errors})
    else:
        return JsonResponse({'status': 'error', 'message': '잘못된 요청 방식입니다.'})


class PassPortfolioUpdate(UpdateView):
    model = PassPortfolio
    template_name = 'pass_portfolio/pass_portfolio_update.html'
    form_class = PassPortfolioForm
    context_object_name = 'pass_portfolio'

    def get_success_url(self):
        return reverse_lazy('pass_portfolio:pass_portfolio_detail', kwargs={'pk': self.object.pk})

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


class PassPortfolioDeleteView(View):
    def post(self, request, pk):
        pass_portfolio = get_object_or_404(PassPortfolio, pk=pk)

        # 권한 확인: 현재 사용자가 포트폴리오 작성자인지 확인
        if request.user == pass_portfolio.author:
            pass_portfolio.delete()
            response_data = {'status': 'success'}
        else:
            response_data = {'status': 'error', 'message': '포트폴리오 삭제 권한이 없습니다.'}

        return JsonResponse(response_data)


class DeleteCommentView(View):
    def post(self, request, pk, comment_id, *args, **kwargs):
        # 댓글을 삭제하는 뷰
        comment = get_object_or_404(PassComment, pk=comment_id)

        # 권한 확인: 현재 사용자가 댓글 작성자인지 확인
        if request.user == comment.user:
            comment.delete()
            return redirect('pass_portfolio:pass_portfolio_detail', pk=pk)
        else:
            return JsonResponse({'status': 'error', 'message': 'No authority to delete'})


@login_required
def toggle_comment_like(request, pk, comment_id):
    comment = get_object_or_404(PassComment, id=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': comment.likes.count()})