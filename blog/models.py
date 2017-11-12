# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.html import strip_tags
from django.utils.six import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import markdown

@python_2_unicode_compatible
class Category(models.Model):
    #文章定义分类
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    #文章标签
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    #文章
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)

    #view字段记录阅读量
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_time', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    #用户访问文章，则views增加1
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    #重写模型的save方法
    def save(self, *args, **kwargs):
        if not self.excerpt:
            #首先实例化一个markdown类，用于渲染body的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:90]
        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)
