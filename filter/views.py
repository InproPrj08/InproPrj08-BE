from django.shortcuts import render
from django.http import HttpResponse
from .models import Student
from django.http import JsonResponse
from .models import Department, SubDepartment
# Create your views here.

def filter_page(request):
    if request.method == 'GET':
        status = request.GET.get('status', '') # 라디오 버튼에서 선택한 상태 값
        interest = request.GET.get('interest', '')

        filtered_students = Student.objects.all()

        if status:  # 상태 값이 전달되었을 때만 필터링
            filtered_students = filtered_students.filter(status=status)
        if interest:
            filtered_students = filtered_students.filter(interest=interest)


        context = {
            'status': status,
            'interest': interest,
            'filtered_students': filtered_students,
        }

        return render(request, 'filter/filter_portfolio.html', context)

    return HttpResponse('Invalid request method')

def populate_database(request):
    data = {}

    # 대학 및 전공 정보 가져오기
    departments = Department.objects.all()
    sub_departments = SubDepartment.objects.all()

    # JSON 데이터 구성
    data['departments'] = [{'id': dep.id, 'name': dep.name} for dep in departments]
    data['sub_departments'] = [{'id': sub.id, 'name': sub.name, 'department_id': sub.department.id} for sub in sub_departments]

    return JsonResponse(data)