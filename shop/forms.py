from django import forms


class CSVImportForms(forms.Form):
    """
    Форма для импорта csv
    """

    csv_file = forms.FileField()
