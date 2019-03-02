#coding:utf-8
from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Article
from .models import Comment
from .forms import CommentForm

# Create your views here.

def article_comment(request,article_pk):
	#使用了Django提供的一个快捷函数 get_object_or_404,文章存在则获取，否则返回404
	article = get_object_or_404(Article,pk = article_pk)
	#http请求有get和post两种，一般用户通过表单提交数据都是通过post请求
	if request.method == 'POST':
		#实例化form表单
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.article = article
			comment.save()
			#实际上当redirect函数接收一个模型的实例时，它会调用这个模型实例的get_absolute_url方法，然后重定向到这个页面
			return redirect(article)
		else:
			comment_list = article.comment_set.all()
			context = {
				'article':article,
				'form':form,
				'comment_list':comment_list
				}
			return render(request,'blog/article_page.html',context=context)
		return redirect(article)