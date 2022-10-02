from django import forms 
from .models import *

class CommentForm(forms.ModelForm):
    

    class Meta:
        model = Comment
        # exclude = ['product', 'user', 'created_on', ]
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'id': 'post-text',
                'required': True,
                'placeholder': 'Make a comment...'
            }),
        }

class BidForm(forms.ModelForm):
    
    
    class Meta:
        model = Bid 
        # exclude = ['user', 'product', 'bid_time']
        fields = ['bid_amount']
        widgets = {
            'bid_amount': forms.NumberInput(attrs={
                'id': 'post-bid',
                'required': True,
                'placeholder': 'Make your bid...'
            }),
        }
    

#class CreateProductForm(forms.Form):

    #class Meta:
        #model = Product

        #fields = ['title', 'image', 'description', 'starting_bid', 'is_active', '']