from django.urls import path, include
from distiller import views as distiller_views
from django.contrib import admin
from django.views.generic.base import TemplateView


class HomeView(TemplateView):

    template_name = 'index.html'

urlpatterns = [
    path('', HomeView.as_view(),),
    path('admin/', admin.site.urls),
    path('distiller/', include('distiller.urls', namespace='distiller')),
    path('findings/', include('resolve_findings.urls', namespace='findings'))
]
