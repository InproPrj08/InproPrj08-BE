from portfolio.models import Major, Portfolio
from django.shortcuts import render



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