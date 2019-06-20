from django.shortcuts import render

def finding_resolution_page(request):
    return render(request, 'resolve_findings/finding-resolution-page.html')
