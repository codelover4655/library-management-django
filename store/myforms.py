from .models import *
from django import forms


class  user_form(forms.ModelForm):
    class Meta:
        model=BookCopy
        fields=['borrow_date','book','borrower']