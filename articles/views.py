from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

@require_GET
def index(request):
   articles = Article.objects.all()
   context = {'articles': articles}
   return render(request, 'articles/index.html', context)
def create(request):
   if request.method == 'POST':
       # Article 을 생성해달라고 하는 요청
       form = ArticleForm(request.POST)
       # embed()
       if form.is_valid():
           form.save()
           return redirect('articles:index')
       # 잘못 입력 되었을 경우 알려줌
       # else:
       #     context = {'form': form}
       #     return render(request, 'articles/create.html', context)
   else: # GET
       # Article 을 생성하기 위한 페이지를 달라고 하는 요청
       form = ArticleForm()
   context = {'form': form}
   return render(request, 'articles/create.html', context)
@require_GET
def detail(request, article_pk):
   # 사용자가 url 에 적어보낸 article_pk 를 통해 디테일 페이지를 보여준다.
   article = get_object_or_404(Article, pk=article_pk)
   comments = article.comments.all()
   form = CommentForm()
   context = {
       'article': article,
       'comments': comments,
       'form': form,
   }
   return render(request, 'articles/detail.html', context)
   # 가능
   # return render(request, 'articles/detail.html', {'article': article})
def update(request, article_pk):
   article = get_object_or_404(Article, pk=article_pk)
   if request.method == 'POST':
       form = ArticleForm(request.POST, instance=article)
       if form.is_valid():
           form.save()
           return redirect('articles:detail', article_pk)
   else:
       # 우와
       form = ArticleForm(instance=article)
   context = {'form':form}
   return render(request, 'articles/update.html', context)
# 받는 method 를 POST 로 제한
@require_POST
def delete(request, article_pk):
   article = get_object_or_404(Article, pk=article_pk)
   # if request.method == 'POST':
   article.delete()
   # 보여줄만한 페이지가 따로 없다...
   return redirect('articles:index')
   # else:
   #     pass
@require_POST
def comments_create(request, article_pk):
   article = get_object_or_404(Article, pk=article_pk)
   form = CommentForm(request.POST)
   if form.is_valid():
       # 임시저장
       comment = form.save(commit=False)
       comment.article_id = article_pk
       comment.save()
       return redirect('articles:detail', article_pk)
   # comment = Comment(article_id = article_pk)
   # form = CommentForm(request.POST, instance=comment)
   # form.save()
@require_POST
def comments_delete(request, article_pk, comment_pk):
   comment = get_object_or_404(Comment, pk=comment_pk)
   comment.delete()
   return redirect('articles:detail', article_pk)