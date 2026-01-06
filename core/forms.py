# core/forms.py
from django import forms
from .models import Review, Listing, Category


class ReviewForm(forms.ModelForm):
    """Form for submitting accessibility reviews"""
    
    class Meta:
        model = Review
        fields = [
            'author_name', 'author_email', 'rating', 'comment',
            'step_free_access', 'restroom_accessible', 'signage_clear',
            'staff_supportive', 'sensory_friendly'
        ]
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'Your name',
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'Email (optional, for follow-up)',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'hidden',
                'min': 1,
                'max': 5,
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none resize-none',
                'placeholder': 'Share your experience... What was accessible? Any challenges?',
                'rows': 4,
            }),
            'step_free_access': forms.NumberInput(attrs={
                'class': 'hidden accessibility-rating',
                'min': 1,
                'max': 5,
            }),
            'restroom_accessible': forms.NumberInput(attrs={
                'class': 'hidden accessibility-rating',
                'min': 1,
                'max': 5,
            }),
            'signage_clear': forms.NumberInput(attrs={
                'class': 'hidden accessibility-rating',
                'min': 1,
                'max': 5,
            }),
            'staff_supportive': forms.NumberInput(attrs={
                'class': 'hidden accessibility-rating',
                'min': 1,
                'max': 5,
            }),
            'sensory_friendly': forms.NumberInput(attrs={
                'class': 'hidden accessibility-rating',
                'min': 1,
                'max': 5,
            }),
        }
        labels = {
            'author_name': 'Your Name',
            'author_email': 'Email (optional)',
            'rating': 'Overall Rating',
            'comment': 'Your Review',
            'step_free_access': 'Step-Free Access',
            'restroom_accessible': 'Accessible Restroom',
            'signage_clear': 'Clear Signage',
            'staff_supportive': 'Helpful Staff',
            'sensory_friendly': 'Sensory Friendly',
        }


class ListingSubmissionForm(forms.ModelForm):
    """Form for users to suggest new accessible venues"""
    
    category_choices = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'category-checkbox',
        }),
        label='Categories'
    )
    
    accessibility_choices = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'accessibility-checkbox',
        }),
        choices=[
            ('wheelchair', 'Wheelchair Accessible'),
            ('braille', 'Braille Signage'),
            ('hearing_loop', 'Hearing Loop'),
            ('accessible_parking', 'Accessible Parking'),
            ('accessible_entrance', 'Accessible Entrance'),
            ('elevator', 'Elevator Available'),
            ('accessible_toilet', 'Accessible Toilet'),
            ('guide_dog_friendly', 'Guide Dog Friendly'),
            ('quiet_space', 'Quiet Space Available'),
            ('large_print', 'Large Print Materials'),
        ],
        label='Accessibility Features'
    )
    
    class Meta:
        model = Listing
        fields = [
            'name', 'subtitle', 'description',
            'address', 'city', 'country',
            'phone', 'website', 'email',
            'price_min', 'price_max', 'status',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'Venue name',
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'Brief tagline (e.g., "Family-friendly café with full wheelchair access")',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none resize-none',
                'placeholder': 'Describe the venue and its accessibility features in detail...',
                'rows': 5,
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'Street address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'City',
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'Country',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': '+1 234 567 8900',
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'https://example.com',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': 'contact@example.com',
            }),
            'price_min': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': '0',
                'min': 0,
            }),
            'price_max': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none',
                'placeholder': '100',
                'min': 0,
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-[#FF431E]/20 focus:border-[#FF431E] outline-none bg-white',
            }),
        }
        labels = {
            'name': 'Venue Name',
            'subtitle': 'Tagline',
            'description': 'Description',
            'address': 'Street Address',
            'city': 'City',
            'country': 'Country',
            'phone': 'Phone Number',
            'website': 'Website',
            'email': 'Contact Email',
            'price_min': 'Minimum Price ($)',
            'price_max': 'Maximum Price ($)',
            'status': 'Current Status',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate category choices from database
        categories = Category.objects.all()
        self.fields['category_choices'].choices = [
            (cat.name, cat.name) for cat in categories
        ]
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Convert selected categories to JSON list
        instance.categories = self.cleaned_data.get('category_choices', [])
        # Convert selected accessibility features to JSON list
        instance.accessibility_features = self.cleaned_data.get('accessibility_choices', [])
        # New submissions go to moderation queue
        instance.moderation_status = 'pending'
        if commit:
            instance.save()
        return instance
