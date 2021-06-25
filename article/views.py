from django.shortcuts import render, redirect

from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.http import HttpResponse

import markdown

def article_list(request):
    # 取出所有的博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（template）的对象
    context = {'articles': articles}

#     render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body, 
                                    extensions=[
                                        # 包含缩写、表格等常用扩展
                                        'markdown.extensions.extra',
                                        # 语法高亮扩展
                                        'markdown.extensions.codehilite',
                                    ])
    context = {'article': article}
    return render(request, 'article/detail.html', context)
    
    
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse('表单内容有误，请重新填写')
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)

def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")


def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求!")
    
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写！")
    else:
        article_post_form = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)