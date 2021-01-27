from django.db import models
from .Category import Category
from django.template.defaultfilters import slugify

class News(models.Model):
    title = models.CharField(max_length=300, db_index=True, unique=True) 
    slug = models.SlugField(max_length=300, db_index=True, unique=True)  
    avatar = models.ImageField(upload_to='static/img/')  
    category = models.ForeignKey(Category, related_name='news', on_delete=models.CASCADE)  
    content = models.TextField(blank=True)
    url = models.URLField(max_length=700) 
    data_added = models.TimeField(auto_now=True)  
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(News, self).save(*args, **kwargs)