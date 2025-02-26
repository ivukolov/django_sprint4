from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('users.urls')),
    path('pages/', include('pages.urls')),
]

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.custom_500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
