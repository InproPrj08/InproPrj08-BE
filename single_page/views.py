import json
from django.shortcuts import render
from portfolio.models import Portfolio
from pass_portfolio.models import PassPortfolio
from recruit.models import Recruit


# Create your views here.
def landing(request):
    # 최근에 작성된 3개의 포트폴리오만 가져오기
    recent_portfolios = Portfolio.objects.all().order_by('-created_at')[:3]
    recent_pass_portfolios = PassPortfolio.objects.all().order_by('-created_at')[:3]
    recent_recruits = Recruit.objects.all().order_by('-created_at')[:3]

    # Process hashtags and convert them to a list
    for portfolio in recent_portfolios:
        portfolio.hashtags = json.loads(portfolio.hashtags)
        portfolio.hashtags = [tag.strip('"') for tag in portfolio.hashtags]  # Remove quotes

        # Process hashtags and convert them to a list
    for pass_portfolio in recent_pass_portfolios:
        pass_portfolio.hashtags = json.loads(pass_portfolio.hashtags)
        pass_portfolio.hashtags = [tag.strip('"') for tag in pass_portfolio.hashtags]  # Remove quotes

    context = {
        'portfolios': recent_portfolios,
        'pass_portfolios': recent_pass_portfolios,
        'recruits': recent_recruits,
    }

    if request.user.username:
        user_portfolios = Portfolio.objects.filter(author__username=request.user.username)
        user_pass_portfolios = PassPortfolio.objects.filter(author__username=request.user.username)
        context.update({
            'pk': user_portfolios[0].pk if user_portfolios else None,
            'pk1': user_pass_portfolios[0].pk if user_pass_portfolios else None,
        })

    print(f"User PK: {request.user.pk}")
    print(f"Context PK1: {context.get('pk1')}")

    return render(request, 'single_page/main_page.html', context)
