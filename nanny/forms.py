from django import forms
from .models import Nanny, Report

#Create your forms here

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length = 50)
    email_address = forms.EmailField(max_length = 150)
    # subject = forms.CharField(max_length =100)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000)


class FilterNannies(forms.Form):
    class Meta:
        model = Nanny
        exclude = ['first_name', 'last_name', 'bio', 'image', 'phonenumber','featured','rate']
        widgets = {
        'pro_skills':forms.CheckboxSelectMultiple(),
        'location':forms.CheckboxSelectMultiple(),
        }

class BookNanny(forms.Form):
    class Meta:
        model = Report
        exclude = ['transaction_id', 'nanny_first_name', 'nanny_last_name', 'nanny_phonenumber', 'nanny_rate','client_id','client_first_name','client_last_name','payment_status','payment_date']
