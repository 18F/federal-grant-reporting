from django import forms


class SingleAuditForm(forms.Form):
    grantee_name = forms.CharField(label="Grant recipient's name", max_length=100)
    grantee_address_line1 = forms.CharField(label='Street address 1', max_length=100)
    grantee_address_line2 = forms.CharField(label='Street address 2', max_length=100)
    grantee_city = forms.CharField(label="City", max_length=100)
