from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.upload),
    path('files/', views.files),
    path('download/', views.download),
    path('finished/', views.finished),
    path('delete/', views.delete),
    path('timings/', views.timings),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
