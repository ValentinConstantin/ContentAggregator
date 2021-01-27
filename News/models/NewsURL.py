from django.db import models
from django.utils.translation import ugettext_lazy as _
from News.GetNews import get_content_from_links, SITES
from .News import News
from .Category import Category
from django.http import HttpResponseRedirect
from django.urls import reverse



class NewsURL(models.Model):
    News_List = (
        ('sport', _('Sport')),
        ('economie', _('Economie')),
        ('politica', _('Politica')),
        ('externe', _('Externe'))
    )
    news = models.CharField(max_length=8, choices=News_List)

    def get_absolute_url(self):
        return reverse("News:list")

    def save(self, *args, **kwargs) -> None:
        for data in get_content_from_links(self.news, SITES, News):
            news_create = News.objects.create(title=data['Title'], avatar="static/img/" + data['Avatar'][-20:] + ".png",
                                              category=Category.objects.get(name=str(self.news).capitalize()),
                                              content=data['Content'], url=data['URL'])
            news_create.save()
        return super().save()
