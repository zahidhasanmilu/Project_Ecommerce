from django import forms
from App_order.models import Order

class BillingAddressForm(forms.Form):
    """BillingAddressForm definition."""

    name = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter name'
        }
    ))
    email = forms.EmailField(label="", required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        }
    ))
    phone = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone'
        }
    ))
    address = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter address'
        }
    ))
    order_note = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter order note',
            'cols': 30,
            'rows': 4,
        }
    ))

class PaymentMethodForm(forms.ModelForm):
    PAYMENT_METHOD = (
        ('Cash On Delivery', 'Cash On Delivery'),
        ('SSL Commerz', 'SSL Commerz'),
    )
    
    """Form definition for PaymentMethod."""
    payment_option = forms.ChoiceField(choices=PAYMENT_METHOD,
        widget=forms.RadioSelect(attrs={
            'class':'collapsed'
        })
    )
    class Meta:
        """Meta definition for PaymentMethodform."""
        model = Order
        fields = ['payment_option',]
