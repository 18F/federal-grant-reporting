from django.shortcuts import render, get_object_or_404
from .models import Finding, Comment
from .forms import CommentForm


def findings_list(request):
    findings = Finding.objects.all()
    return render(request,
                  'resolve_findings/list.html',
                  {'findings': findings})


def finding_resolution_page(request, finding_id):
    finding = get_object_or_404(Finding, id=finding_id)

    comments = finding.comments.filter(is_published=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.finding = finding
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'finding': finding,
        'comments': comments,
        'comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'resolve_findings/finding-resolution-page.html', context)
