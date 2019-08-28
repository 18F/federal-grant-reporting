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
from django.contrib import admin
from django.urls import path
# from fac import views  # @todo: Revisit, split out by app.
from fac.views import get_single_audit_package
from distiller import views as distiller_views
from resolve_findings import views as findings_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fac', get_single_audit_package),
    path('', distiller_views.prompt_for_agency_name),
    path('get-single-audits-by-agency/', distiller_views.show_agency_level_summary, name='show_relevant_audits'),
    path('generate-a-csv/', distiller_views.offer_download_of_agency_specific_csv, name='prompt_to_save_csv'),
    path('download-single-audits/', distiller_views.download_files_from_fac, name='download_single_audit_pdfs'),
    path('findings/', findings_views.findings_list, name='findings_overview'),
    path('finding/<int:finding_id>/', findings_views.finding_resolution_page, name='finding'),
]
