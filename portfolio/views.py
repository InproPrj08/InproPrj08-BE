from django.shortcuts import render, redirect
from .models import Portfolio
from django.views.generic import ListView, DetailView
# Create your views here.

class PortfolioList(ListView):
    model = Portfolio
    ordering = '-pk'


class PortfolioDetail(DetailView):
    model = Portfolio


def like(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    if (portfolio.like_users.filter(pk=request.user.pk)):
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
