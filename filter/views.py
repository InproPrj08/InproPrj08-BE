from django.shortcuts import render
from .models import Student
# Create your views here.

def filter_portfolio(request):
    if request.method == 'GET':
        status = request.GET.get('status', '')
        if status:
            students = Student.objects.filter(status=status)
        else:
            students = Student.objects.all()

        return render(request, 'filter_portfolio.html', {'students': students})