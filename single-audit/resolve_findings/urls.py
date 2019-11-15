from django.urls import path
from .views import findings_list, finding_resolution_page

app_name = 'resolve_findings'
urlpatterns = [
    path('<int:finding_id>/', finding_resolution_page, name='details'),
    path('', findings_list, name='list')
]
