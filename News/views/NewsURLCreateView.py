from News.models.NewsURL import NewsURL
from django.views.generic.edit import CreateView
from News.forms.AddNewsURL import AddNewsURL


class NewsURLCreateView(CreateView):
    model = NewsURL
    template_name = "news_url_add.html"
    form_class = AddNewsURL
