from django import forms


class UploadFileForm(forms.Form):
    score_data = forms.ChoiceField(widget=forms.RadioSelect,
                                   initial='ucsc15',
                                   choices=[('ucsc15', 'UCSC15WAY'),
                                            ('vista12', 'VISTA12WAY'),
                                            ('vista6', 'VISTA6WAY')])
    upload_file = forms.FileField()
