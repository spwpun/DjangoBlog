# coding:utf-8
from django import template
from ..models import Article,Category,Tag
from django.db.models.aggregates import Count


register = template.Library()

@register.simple_tag
def get_recent_articles(num=5):
	return Article.objects.all().order_by('-pub_time')[:num]

@register.simple_tag
def archives():
	#这里dates方法会返回一个列表，列表中元素为每一篇文章创建的时间，且是python的date对象，精确到月份，降序排列
	return Article.objects.dates('pub_time','month',order='DESC')

@register.simple_tag
def get_categories():
	return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)

@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
