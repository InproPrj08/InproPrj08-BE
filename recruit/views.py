import traceback
from datetime import datetime
from os.path import basename

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View

from portfolio.models import Status, College
from .models import Comment, Interest, Major, Recruit
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import CommentForm, RecruitForm


# Create your views here.
class RecruitList(ListView):
    model = Recruit
    template_name = 'recruit_list.html'
    paginate_by = 6  # 페이지당 보여질 아이템 수
    page_kwarg = "page"
    def get_queryset(self):
        return Recruit.objects.all().order_by('-created_at')


class RecruitDetail(DetailView):
    model = Recruit
    template_name = 'recruit/recruit_detail.html'
    context_object_name = 'recruit'

    def download_file(self, filename, content, content_type):
        response = HttpResponse(content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        recruit = self.object

        # 요청이 파일 다운로드인지 확인
        download_file_type = request.GET.get('download')
        if download_file_type == 'file':
            # 포트폴리오의 파일 내용 다운로드
            file_content = recruit.file.read()
            return self.download_file(f"{recruit.title}.{recruit.file.name.split('.')[-1]}", file_content, 'application/octet-stream')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recruit = self.object  # 현재 포트폴리오 객체 사용

        context['comments'] = Comment.objects.filter(recruit=recruit).order_by('-created_at')
        context['form'] = CommentForm()

        # 특정 포트폴리오 객체를 사용하여 추가 데이터를 가져옵니다.
        if recruit:

            if recruit.file:
                file_name = basename(recruit.file.name)
            else:
                file_name = None

            interests = recruit.interest_field.all()
            interest_names = [interest.interest for interest in interests]

            context['text_data'] = {
                'title': recruit.title,
                'content': recruit.content,
                'styles': recruit.styles,
                'interest_field': interest_names,
                'department': recruit.department.name if recruit.department else None,
                'status': recruit.status,
                'people': recruit.people,
                'deadline': recruit.deadline,
                'file': recruit.file,
                'file_name':file_name,
            }
            print(recruit.interest_field)
        else:
            context['text_data'] = None

        return context

    def post(self, request, pk):
        recruit = get_object_or_404(Recruit, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.recruit = recruit
            if request.user.is_authenticated:
                comment.user = request.user
                if comment.user == recruit.author:  # 포트폴리오 작성자와 댓글 작성자가 동일한 경우
                    comment.is_recruit_author = True
            else:
                comment.is_anonymous = True  # 예시 코드, 실제로 사용하려면 Comment 모델에 is_anonymous 필드를 추가해야 함

            comment.save()
            # 댓글을 작성한 후에 PortfolioDetail 페이지로 리디렉션
            return redirect('recruit:recruit_detail', pk=recruit.pk)
        else:
            return self.form_invalid(form)



def search_view(request):
    query = request.GET.get('q')

    if query:
        results = Recruit.objects.filter(title__icontains=query)  # 검색어가 제목에 포함된 경우
    else:
        results = Recruit.objects.all()

    return render(request, 'recruit/search_results.html', {'results': results, 'query': query})



def your_combined_view(request):
    if request.method == 'POST':
        form = RecruitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_text/')
    else:
        form = RecruitForm()

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

    return render(request, 'recruit/index.html', context)


def save_text(request):
    if request.method == 'POST':
        form = RecruitForm(request.POST, request.FILES)
        print(form.data)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            styles = form.cleaned_data['styles']
            department = form.cleaned_data['department']
            status_value = form.cleaned_data['status']
            status = status_value
            file = form.cleaned_data['file']
            people = form.cleaned_data['people']
            deadline = form.cleaned_data['deadline']

            # 서버에서 하드코딩하여 한국 시간으로 설정
            timezone_korea = timezone.get_fixed_timezone(9 * 60)  # 9 hours ahead of UTC
            deadline = timezone.localtime(deadline, timezone_korea)

            interest_field_ids = form.cleaned_data.get('interest_field')
            interest_instances = Interest.objects.filter(id__in=interest_field_ids)

            recruit_instance = Recruit(
                title=title,
                content=content,
                styles=styles,
                department=department,
                status=status,
                author=request.user,
                file=file,
                people=people,
                deadline=deadline,  # Set the corrected deadline here
            )

            # D-day 값 계산 및 저장
            recruit_instance.d_day = recruit_instance.calculate_d_day()
            recruit_instance.save()

            if interest_instances:
                recruit_instance.interest_field.set(interest_instances)

            return JsonResponse({'status': 'success', 'pk': recruit_instance.pk})
        else:
            print(form.errors)
            return JsonResponse({'status': 'error', 'message': '폼이 유효하지 않습니다.', 'errors': form.errors})
    else:
        return JsonResponse({'status': 'error', 'message': '잘못된 요청 방식입니다.'})


class RecruitUpdate(UpdateView):
    model = Recruit
    template_name = 'recruit/recruit_update.html'
    form_class = RecruitForm
    context_object_name = 'recruit'

    def get_success_url(self):
        return reverse_lazy('recruit:recruit_detail', kwargs={'pk': self.object.pk})

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

class RecruitDeleteView(View):
    def post(self, request, pk):
        recruit = get_object_or_404(Recruit, pk=pk)

        # 권한 확인: 현재 사용자가 포트폴리오 작성자인지 확인
        if request.user == recruit.author:
            recruit.delete()
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
            return redirect('recruit:recruit_detail', pk=pk)
        else:
            return JsonResponse({'status': 'error', 'message': 'No authority to delete'})


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