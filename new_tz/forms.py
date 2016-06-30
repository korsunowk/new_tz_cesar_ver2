from django import forms

class Form(forms.Form):
    text = forms.CharField(
        required=True, 
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Введите текст',
                'required':'required',
                'id':"text1",
                'rows':"16",
                'cols':"100"
                }
            )
        )
    key = forms.IntegerField(
        required=True,
        min_value=0,
        max_value=25, 
        widget=forms.NumberInput(
            attrs={
                'required':'required',
                'id':'key',
                'class':"rot_inp"
                }
            )
        )
