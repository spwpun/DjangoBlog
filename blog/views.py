# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import models
import datetime
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.db.models import Q
# Create your views here.

# 上面的index函数和下面的类IndexView实现的是同一个功能，只是下面的是基于类的通用视图，使用起来更好管理
class IndexView(ListView):
	model = models.Article
	template_name = 'blog/index.html'
	context_object_name = 'articles'
	# 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
	paginate_by = 5

	def get_queryset(self):
		return super(IndexView,self).get_queryset().order_by('-id')

#article_page的通用类视图
class ArticleView(DetailView):
	model = models.Article
	template_name = 'blog/article_page.html'
	context_object_name = 'article'
	#覆盖get方法的原因是因为每次文章被访问，就要将阅读数加一
	def get(self,request,*args,**kwargs):
		#get 方法返回的是一个HTTPResponse实例
		response = super(ArticleView,self).get(request,*args,**kwargs)
		#将文章阅读量加1
		self.object.increase_views()
		return response
	
	def get_object(self,queryset=None):
		#渲染content
		article = get_object_or_404(models.Article,id = self.kwargs.get('article_id'))
		md = markdown.Markdown(extensions=[
										 'markdown.extensions.extra',
										 'markdown.extensions.codehilite',
										 TocExtension(slugify=slugify),
										 ])
		article.content = md.convert(article.content)
		article.toc = md.toc
		article.save()
		return article

	#将评论表单、评论列表传递给模板
	def get_context_data(self,**kwargs):
		context = super(ArticleView,self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
			'form':form,
			'comment_list':comment_list
			})
		return context

#archives的通用类视图
class ArchivesView(IndexView):
	#重写方法实现归档
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(pub_time__year=year,
                                                               pub_time__month=month
                                                               )

#catrgory的通用类视图
class CategoryView(IndexView):
	#复写查询集合的方法，按归类查询，因为原来的get_queryset方法获取的是全部的数据
	def get_queryset(self):
		cate = get_object_or_404(models.Category,pk = self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)

#Tag显示标签下的文章
class TagView(IndexView):

    def get_queryset(self):
        tag = get_object_or_404(models.Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

'''
#搜索的响应函数
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    articles = models.Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'articles': articles})
'''

def about(request):
	return render(request,'blog/about.html')

def contact(request):
	return render(request,'blog/contact.html')