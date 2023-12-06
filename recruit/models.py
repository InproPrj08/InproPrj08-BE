from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from portfolio.models import Interest, Major, CUser
from model_utils.fields import MonitorField


#포트폴리오

class Recruit(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    styles = models.JSONField(blank=True, null=True)
    interest_field = models.ManyToManyField(Interest, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    department = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True)
    people = models.IntegerField()
    author = models.ForeignKey('portfolio.CUser', on_delete=models.CASCADE, related_name='recruit_entries')
    file = models.FileField(upload_to='recruit/files/%Y/%m/%d/', blank=True)
    deadline = models.DateTimeField()
    d_day = models.IntegerField(default=0)
    deadline_changed = MonitorField(monitor='deadline')
    like_users = models.ManyToManyField(CUser, blank=True, related_name='like_recruit')

    def __str__(self):
        return f'☆{self.pk}☆{self.title} :: {self.author}'

    def get_absolute_url(self):
        return reverse('recruit:recruit_detail', kwargs={'pk': self.pk})

    def update(self, new_title, new_content):
        self.title = new_title
        self.content = new_content
        # 다른 필드들도 필요에 따라 업데이트
        self.save()

    def delete(self, *args, **kwargs):
        # 필요에 따라 다른 연관된 객체들도 삭제
        super().delete(*args, **kwargs)

    def calculate_d_day(self):
        now = timezone.now()
        end_of_day = now.replace(hour=23, minute=59, second=59)
        return (self.deadline - end_of_day).days


# pre_save 신호 핸들러
@receiver(pre_save, sender=Recruit)
def update_d_day(sender, instance, **kwargs):
    # 마감기한이 변경되었을 때 D-day 업데이트
    if instance.deadline_changed:
        instance.d_day = instance.calculate_d_day()

# 신호를 연결
pre_save.connect(update_d_day, sender=Recruit)


#댓글
class Comment(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    user = models.ForeignKey(CUser, on_delete=models.CASCADE, related_name='recruit_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    likes = models.ManyToManyField(CUser, related_name='recruit_comment_likes', blank=True)
