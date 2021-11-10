from django.db import models


class News(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name="新闻标题")
    summary = models.TextField(max_length=400, null=True, blank=True, verbose_name="新闻简介")
    detail_url = models.CharField(max_length=250, null=True, blank=True, verbose_name="新闻详情链接")
    img_url = models.CharField(max_length=350, null=True, blank=True, verbose_name="新闻插图链接链接")
    tag = models.CharField(max_length=20, null=True, blank=True, verbose_name="新闻分类标签")

    class Meta:
        db_table = "news"
        verbose_name = "汽车之家-新闻数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
