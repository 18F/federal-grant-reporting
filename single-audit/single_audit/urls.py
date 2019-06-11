"""single_audit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
# from fac import views  # @todo: Revisit, split out by app.
from fac.views import get_single_audit_package
from distiller import views
from resolve_findings.views import finding_resolution_page

urlpatterns = [
    path('fac', get_single_audit_package, name='FAC'),
    path('', views.prompt_for_agency_name, name='Distiller'),
    path('finding-resolution-page', finding_resolution_page),
    path('get-single-audits-by-agency/', views.show_agency_level_summary, name='Show relevant single audits'),
    path('generate-a-csv/', views.offer_download_of_agency_specific_csv, name='Prompt to save a CSV'),
]
