from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.upload),
    path('files/', views.file_list),
    path('download/', views.download),
    path('file_done/', views.file_done),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
