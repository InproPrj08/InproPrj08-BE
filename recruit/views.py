import json

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError
from .models import YourModel

from .forms import YourModelForm

# def your_view(request):
#     if request.method == 'POST':
#         form = YourModelForm(request.POST)
#         if form.is_valid():
#             form.save()  # 폼이 유효하면 데이터를 저장
#             return redirect('display_text/')  # 원하는 페이지로 리다이렉트
#     else:
#         form = YourModelForm()
#
#     return render(request, 'recruit/templates.html', {'form': form})
#
# def index(request):
#
#     return render(
#         request,
#         'recruit/index.html',
#     )

def your_combined_view(request):
    if request.method == 'POST':
        form = YourModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_text/')
    else:
        form = YourModelForm()

    return render(request, 'recruit/index.html', {'form': form})


def save_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_input = data.get('content', '')
            styles = data.get('styles', None)

            print('Received data:', data)  # 이 줄을 추가합니다

            YourModel.objects.create(content=user_input, styles=styles)

            return JsonResponse({'status': 'Text successfully saved.', 'user_input': user_input})
        except json.JSONDecodeError as e:
            print(f'JSON Decode Error: {str(e)}')  # 이 줄을 추가합니다
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def display_text(request):
    all_texts = YourModel.objects.all()
    if all_texts.exists():
        stored_text = all_texts.all()
        print(stored_text)
    else:
        stored_text = None
    return render(request, 'recruit/template.html', {'stored_text': stored_text})
# Create your views here.
