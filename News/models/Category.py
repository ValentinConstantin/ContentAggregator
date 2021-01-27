from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(_('Category name'), max_length=50, unique=True)
    slug = models.SlugField(_('Category slug'), max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

    def get_absolut_url(self):
        return reverse('News:list_by_category', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)