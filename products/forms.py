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
    
    