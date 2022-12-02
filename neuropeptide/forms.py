from django import forms


class add_task(forms.Form):
    name = forms.CharField(label="Name",
                           required=False,
                           max_length=200,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email",
                             required=True,
                             error_messages={"required": u"Email is the only way we can notify you and is required."},
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    data = forms.CharField(label="Data",
                           required=False,
                           widget=forms.Textarea(attrs={"class": "form-control", "rows": "6", "style": "resize:none"}))
    file = forms.FileField(label="Fasta File",
                           required=False,
                           widget=forms.FileInput(attrs={"style": "display:none;", "id": "fasta_file"}))
