# Django 실습
##### Date 2020_12_6
---
### CommentApp 마무리
> 1. 댓글 출력
> acticleapp의 detail.html을 수정한다.
> 
> 지금은 댓글을 다는것만 가능하고 
> 
> 달려있는 댓글을 볼 수 없기 때문이다.
> 
> 먼저 ```{% include 'commentapp/create.html' with article=target_article %}```의 위에
> ```html
> {% for comment in target_article.comment.all %}
>             <!--target_article.comment.all = target_article에 외래키로 연결되어 있는 댓글을 전부 가져온다.-->
>                 {% include 'commentapp/detail.html' with comment=comment %}
>             {% endfor %}
> ```
> 위의 코드를 추가한다.
> 
> 그 다음 commentapp에 detail.html를 생성하고 아래와 같이 작성한다.
> ```html
> <div style="border: 1px solid; text-align: left; padding: 4%; margin: 1rem 0; border-radius: 1rem; border-color: #bbb;">
>     <div>
>         <strong>
>             {{ comment.writer.profile.nickname }}
>             <!--닉네임-->
>         </strong>
>         &nbsp&nbsp&nbsp
>         {{ comment.create_at }}
>         <!--댓글 작성한 날-->
>     </div>
>     <div style="margin:  1rem 0">
>         {{ comment.content }}
>         <!--댓글 내용-->
>     </div>
> </div>
> ```
> 
> 2. 삭제기능 추가
> commentapp의 views.py에 삭제 기능구현을 위한 코드를 작성한다.
> ```Python
> class CommentDeleteView(DeleteView):
>     model = Comment
>     context_object_name = 'target_comment'
>     template_name = 'commentapp/delete.html'
> 
>     def get_success_url(self):
>         return reverse('articleapp:detail', kwargs={'pk': self.object.article.pk})
> ```
> 다음으로는 댓글에 삭제 버튼을 생성한다.
> 
> detail.html의 맨 아래에 있는 {% endif %}위에 작성한다.
> ```html
>     <div style="text-align: right">
>         <a href="{% url 'commentapp:delete' pk=comment.pk %}"class="btn btn-danger rounded-pill">
>             삭제
>         </a>
>     </div>
> ```
> 다음으로 delete.html을 아래와 같이 작성한다.
> ```Python
> {% extends 'base.html' %}
> {% load bootstrap4 %}
> 
> {% block content %}
> 
>     <div style="text-align: center; max-width: 500px; margin: 4rem auto;">
>         <div class="mb-4">
>             <h4>댓글 삭제 : {{ target_comment.content }}</h4>
>         </div>
>         <form action="{% url 'commentapp:delete' pk=target_comment.pk %}" method="post">
>             {% csrf_token %}
>               <input type="submit" class="btn btn-danger rounded-pill col-6 mt-3">
>         </form>
>     </div>
> 
> {% endblock %}
> ```
> 
> 아 물론 urls.py에 ```path('delete/<int:pk>', CommentDeleteView.as_view(), name='delete'),```는 추가해야한다.
> 
> 마지막으로는 decorators.py를 생성하고 적용시켜 주어야한다.
> ```Python
> from django.http import HttpResponseForbidden
> from commentapp.models import Comment
> 
> def comment_ownership_required(func):
>     def decorated(request, *args, **kwargs):
>         comment = Comment.objects.get(pk=kwargs['pk'])
>         # 요청을 받으며 pk로 받은 값을 가지고 있는 User.objects가 profile이 된다.
>         if not comment.writer == request.user: #그 article request의 profile이 아니라면
>             return HttpResponseForbidden() #권한없음 창 띄움.
>         return func(request, *args, **kwargs)
>     return decorated
> ```
> 위와같이 decorators.py 를 작성하고 views.py에도 적용시켜준다.
> CommentDeleteView클래스 위에 아래의 코드를 추가한다.
> ```Python
> @method_decorator(comment_ownership_required, 'get')
> @method_decorator(comment_ownership_required, 'post')
> ```
# 끝!
오늘은 [38강](https://www.youtube.com/watch?v=egXJzs06f3Q&list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo&index=39)의 학습을 진행 하였다.
## 참고한 영상 : [실용주의 프로그래머의 작정하고 장고! Django로 Pinterest 따라하기](https://www.youtube.com/playlist?list=PLQFurmxCuZ2RVfilzQB5rCGWuODBf4Qjo)
