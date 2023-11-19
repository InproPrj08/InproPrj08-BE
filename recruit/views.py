from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import YourModel

from .forms import YourModelForm

def your_view(request):
    if request.method == 'POST':
        form = YourModelForm(request.POST)
        if form.is_valid():
            form.save()  # 폼이 유효하면 데이터를 저장
            return redirect('display_text/')  # 원하는 페이지로 리다이렉트
    else:
        form = YourModelForm()

    return render(request, 'recruit/templates.html', {'form': form})

def index(request):
    return render(
        request,
        'recruit/index.html',
    )

def save_text(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        # 여기에서 user_input을 사용하여 모델에 저장하는 작업 수행
        YourModel.objects.create(content=user_input)
        return JsonResponse({'status': 'Text successfully saved.', 'user_input': user_input})
    return JsonResponse({'status': 'error'})

def display_text(request):
    all_texts = YourModel.objects.all()
    if all_texts.exists():
        stored_text = all_texts.all()
    else:
        stored_text = None
    return render(request, 'recruit/template.html', {'stored_text': stored_text})
# Create your views here.
