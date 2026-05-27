from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import GymClass, Trainer


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:classes', 'core:schedule', 'core:trainers', 'core:exercises', 'core:gallery', 'core:about']

    def location(self, item):
        return reverse(item)


class ClassSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return GymClass.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('core:classes') + f'?category={obj.category}'


class TrainerSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Trainer.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('core:trainer_detail', kwargs={'slug': obj.slug})
