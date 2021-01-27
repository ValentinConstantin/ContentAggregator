from django.views.generic.detail import DetailView
from News.models import News


class NewsView(DetailView):
    model = News
    template_name = "news_detail.html"
    slug_field = "slug"
