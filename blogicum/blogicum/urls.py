from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('auth/', include('users.urls')),
    path('pages/', include('pages.urls')),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.custom_500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    ) 
