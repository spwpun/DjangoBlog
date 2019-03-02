# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
import markdown
from django.urls import reverse
from django.utils.html import strip_tags

# Create your models here. One model can be regarded as a class, or like a data table.

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Article(models.Model):
	# 继承Model类
	title = models.CharField(max_length=32,default= 'Title')	# 文章标题
	content = models.TextField(null = True)		# 文章内容
	pub_time = models.DateTimeField(default=datetime.datetime.now())
	modified_time = models.DateTimeField(default=datetime.datetime.now())
	
	abstract = models.CharField(max_length=200, null=True)

	category = models.ForeignKey(Category,on_delete=models.DO_NOTHING) #ForeignKey means ManyToOne's relationships.
	tags = models.ManyToManyField(Tag)
	author = models.ForeignKey(User,on_delete=models.DO_NOTHING, null=True) #User is the default table of django for administrate website.
	views = models.PositiveIntegerField(default=0) #新views字段记录阅读量

	def __str__(self):
		return self.title

	# 自定义 get_absolute_url 方法,得到当前对象的url路径
    # 记得从 django.urls 中导入 reverse 函数
	def get_absolute_url(self):
		return reverse('blog:article_page', kwargs={'article_id': self.id})

	# 自定义increase_views方法来对该篇文章的阅读量做一个大概的统计
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	# 复写save方法来实现自动添加摘要
	def save(self,*args,**kwargs):
		#如果没有填写摘要
		if not self.abstract:
			#首先要实例化一个Markdown 类，用于渲染body的文本
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite',
				])
			#先将content中的markdown文本转换为html，去掉html中的标签（这里用到的方式是strip_tags）,然后再截取前54个字符
			self.abstract = strip_tags(md.convert(self.content))[:54]
		super(Article,self).save(*args,**kwargs)

