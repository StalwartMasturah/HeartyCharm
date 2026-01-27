from django import forms

class CustomOrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    product_description = forms.CharField(widget=forms.Textarea)
    quantity = forms.IntegerField(min_value=1)
    budget = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    deadline = forms.DateField(required=False)
    reference_image = forms.FileField(required=False)
    additional_notes = forms.CharField(widget=forms.Textarea, required=False)
    agree_terms = forms.BooleanField(label="I agree to the terms and conditions")
    subscribe_newsletter = forms.BooleanField(label="Subscribe to newsletter", required=False)
    preferred_contact_method = forms.ChoiceField(choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
    ], widget=forms.RadioSelect)
    best_time_to_contact = forms.ChoiceField(choices=[
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ], widget=forms.RadioSelect, required=False)
    referral_source = forms.ChoiceField(choices=[
        ('social_media', 'Social Media'),
        ('friend_family', 'Friend/Family'),
        ('search_engine', 'Search Engine'),
        ('other', 'Other'),
    ], required=False)
    
    
class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )

    phone = forms.RegexField(
    regex=r'^\d{11}$',
    max_length=11,
    error_messages={
        'invalid': 'Enter a valid 11-digit phone number'
    },
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number',
        'type': 'tel',
        'inputmode': 'numeric',
        'pattern': '[0-9]*'
    })
)

    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Additional Notes you want us to consider regarding your orders, if you want a diffrent color or reduce size (optional)',
            'rows': 3
        }),
        required=False
    )
    street = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Street Address (e.g. 12 Allen Avenue)'
        })
    )

    town = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Town / Area (e.g. Ikeja)'
        })
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(e.g. Lagos)'
        })
    )
    landmark = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nearest Landmark (optional)'
        })
    )

    postal_code = forms.RegexField(
        regex=r'^\d{5,6}$',
        error_messages={
            'invalid': 'Enter a valid postal code'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Postal Code',
            'inputmode': 'numeric',
            'pattern': '[0-9]*'
        })
    )
    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(e.g. Nigeria)'
        })
    )