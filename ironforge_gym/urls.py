from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, ClassSitemap, TrainerSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'classes': ClassSitemap,
    'trainers': TrainerSitemap,
}

admin.site.site_header = "IronForge Admin"
admin.site.site_title = "IronForge Gym Portal"
admin.site.index_title = "Welcome to IronForge Control Center"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('manage/', include('admin_panel.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
