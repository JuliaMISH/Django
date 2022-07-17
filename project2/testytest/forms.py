from django import forms


from testytest.models import Product


class ProductForm(forms.ModelForm):
    title       = forms.CharField(label = 'Title', widget=forms.TextInput(attrs={"placeholder": "My_title"}), initial= "Awesome title")
    description = forms.CharField(
        required=False,
        label = 'Description',
        widget=forms.Textarea(
            attrs={
                "placeholder": "My_description",
                "class": 'new-class-name two',
                "id": "my-id-for-textarea",
                "rows": 20,
                "cols": 120
            }
        )
    )
    price       = forms.DecimalField(initial=15.00)


    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]