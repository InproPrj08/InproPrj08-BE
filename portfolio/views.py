from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Portfolio, Comment
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import CommentForm, PortfolioForm
# Create your views here.

# class PortfolioList(ListView):
#     model = Portfolio
#     ordering = '-pk'
class PortfolioList(ListView):
    model = Portfolio
    template_name = 'portfolio_list.html'
    paginate_by = 6  # 페이지당 보여질 아이템 수
    page_kwarg = "page"
    def get_queryset(self):
        return Portfolio.objects.all().order_by('-created_at')

class PortfolioDetail(DetailView):
    model = Portfolio
    template_name = 'portfolio/portfolio_detail.html'
    context_object_name = 'portfolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 여기서 self.object를 사용하여 포트폴리오 객체에 접근할 수 있습니다.
        context['comments'] = Comment.objects.filter(portfolio=self.object).order_by('-created_at')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.portfolio = self.object
            comment.user = self.request.user  # Assuming user is authenticated
            comment.is_anonymous = request.POST.get('is_anonymous') == 'on'
            comment.save()

            # 댓글을 작성한 후에 PortfolioDetail 페이지로 리디렉션
            return redirect('portfolio_detail', pk=self.object.pk)
        else:
            return self.form_invalid(form)


@login_required
def like(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if portfolio.like_users.filter(pk=request.user.pk):
        portfolio.like_users.remove(request.user)
    else:
        portfolio.like_users.add(request.user)
    return redirect(portfolio.get_absolute_url())


def search_view(request):
    query = request.GET.get('q')

    if query:
        results = Portfolio.objects.filter(title__icontains=query)  # 검색어가 제목에 포함된 경우
    else:
        results = Portfolio.objects.all()

    return render(request, 'portfolio/search_results.html', {'results': results, 'query': query})


