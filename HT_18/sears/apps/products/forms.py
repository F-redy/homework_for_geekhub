from django import forms


class AddProductForm(forms.Form):
    user_input = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'text-products',
                'cols': 80,
                'rows': 12,
                'placeholder': 'Enter ID separated by new line(example):\n'
                               'p-00935112000P\np-A075482002\np-00937537000P\np-A119540351\n'
                               'p-0000000000000000697300000000000007464308P\np-A116635279\n'
                               'p-SPM10450584608\np-A085642481\np-00602692000P\np-A011991588\np-A119988757',
                'required': True
            }
        )
    )
