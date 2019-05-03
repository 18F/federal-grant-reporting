from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SingleAuditForm


def get_single_audit_package(request):
    if request.method == 'POST':
        form = SingleAuditForm(request.POST)

        if form.is_valid():
            # @todo: Process the data in form.cleaned_data.
            # For the moment, this may mean: delete it so
            # we don't risk accidentally storing PII.
            #
            # @todo: Make the confirmation page.
            return HttpResponseRedirect('/confirmation/')

    else:
        form = SingleAuditForm()

    return render(request, 'fac.html', {'form': form})
