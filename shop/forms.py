from django import forms


class CSVImportForms(forms.Form):
    csv_file = forms.FileField()
