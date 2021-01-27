from django.shortcuts import render, get_object_or_404, redirect
from News.models import Category, News


def news_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    news_list = News.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        news_list = News.objects.filter(available=True)
        news_list = news_list.filter(category=category)

    return render(request,
                  'news_list.html',
                  {'category': category,
                   'categories': categories,
                   'newsList': news_list})