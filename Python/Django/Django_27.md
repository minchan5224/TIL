# Django 프로젝트
##### Date 2020_12_19
원래 오늘은 댓글과 프로젝트(뭐랄까 카테고리? 가 가장 적절하네요) 만들려고 했습니다.

하지만 그냥 그렇게 하는것보다 댓글에 대댓글(댓글의 댓글)을 구현 하는게 더 좋을 것이라는 생각이 들었습니다.

그래서 만들었습니다.

---

### 당연히 startapp 해야겠죠
기본적인 과정은 [Django_18](https://github.com/minchan5224/TIL/blob/main/Python/Django/Django_18.md)과 동일하게 하였습니다.

댓글은 commentapp. 대댓글은 recommentapp으로 만들었습니다.

여기서 각각의 코드는 아래와 같이 작성하였습니다.
1. commentapp
#### models.py
```Python
from django.contrib.auth.models import User
from django.db import models
from articleapp.models import Article

# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='comment')
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment')

    content = models.TextField(null=False)

    create_at = models.DateTimeField(auto_now=True)
```
#### urls.py
```Python
from django.urls import path
from commentapp.views import CommentCreateView, CommentDeleteView, CommentDetailView

app_name = 'commentapp'

urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='create'),
    path('delete/<int:pk>', CommentDeleteView.as_view(), name='delete'),
    path('detail/', CommentDetailView.as_view(), name='detail'),
]
````
#### views.py
```Python
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView

from commentapp.forms import CommentCreationForm
from commentapp.models import Comment
from articleapp.models import Article

from commentapp.decorators import comment_ownership_required
from django.utils.decorators import method_decorator

from recommentapp.forms import RecommentCreationForm
from django.views.generic.edit import FormMixin

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreationForm
    template_name = 'commentapp/create.html'

    def form_valid(self, form):
        temp_comment = form.save(commit=False) #임시 저장
        temp_comment.article = Article.objects.get(pk=self.request.POST['article_pk'])
        # 리퀘스트에서 받은 post데이터중 article_pk라는 데이터를 article값으로 설정해주는것
        # 즉 create.html에서 hidden으로 보낸 article.pk가 이쪽으로 넘어 오는것
        temp_comment.writer = self.request.user
        temp_comment.save() # 최종적으로 저장
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.article.pk})
        # object(comment)의 article의 pk를 가진 detail로 되돌아 가는것.

@method_decorator(comment_ownership_required, 'get')
@method_decorator(comment_ownership_required, 'post')
class CommentDeleteView(DeleteView):
    model = Comment
    context_object_name = 'target_comment'
    template_name = 'commentapp/delete.html'

    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk': self.object.article.pk})

class CommentDetailView(ListView):
    model = Comment
    context_object_name = 'target_comment'
    template_name = 'commentapp/detail.html'
    paginate_by = 2
```
