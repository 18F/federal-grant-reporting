from django.shortcuts import render, get_object_or_404
from .models import Finding


def findings_list(request):
    findings = Finding.objects.all()
    return render(request,
                  'resolve_findings/list.html',
                  {'findings': findings})


def finding_resolution_page(request, finding_id):
    finding = get_object_or_404(Finding, id=finding_id)
    context = {
        'finding': finding
    }
    return render(request, 'resolve_findings/finding-resolution-page.html', context)
