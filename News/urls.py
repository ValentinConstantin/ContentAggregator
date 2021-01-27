from django.urls import path
from .views import *

app_name = "News"

urlpatterns = [
    path("add", NewsURLCreateView.as_view(), name="add"),
    path('', news_list, name='list'),
    path('<slug:category_slug>', news_list, name='list_by_category'),
    path('<slug>/detail', NewsView.as_view(), name="detail")
]
