from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['construction_type', 'start_at', 'end_at','content']
        # widgets = {
        #     'start_at': forms.DateInput(attrs={'type': 'date'}),
        #     'end_at': forms.DateInput(attrs={'type': 'date'}),
        # }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                profile = user.profile
                self.initial['department'] = profile.department
                self.initial['agency'] = profile.agency
                self.initial['phone'] = profile.phone
            except User.profile.RelatedObjectDoesNotExist:
                pass
