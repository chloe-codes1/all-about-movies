# movies/forms.py
from django import forms
from .models import Movie, Comment, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        label='Title',
        help_text='Your title must be no more than 100 characters in length',
        widget=forms.TextInput(
            attrs={
                'class':'my_input',
                'placeholder': "Write Title of Your Review"
            }
        )
    )

    content = forms.CharField(
        label='Content',
        help_text='Write your review about movie',
        widget=forms.Textarea(
            attrs={
                'row':5,
                'col':50,
            }
        )
    )

    rating = forms.IntegerField(
        label='Rank',
        help_text='range from 0 to 5',
        widget=forms.NumberInput(
                attrs={
                'type':'range',
                'class': 'custom-range',
                'min': '0',
                'max' :'5',
            }
        )
    )
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating', 'image']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=100,
        label='Comment Content',
        help_text='Your comment must be no more than 100 characters in length',
        widget=forms.TextInput(
            attrs={
                'class':'input-sm',
                'placeholder': "What do you think about this review?"
            }
        )
    )
    class Meta:
        model = Comment
        fields = ['content']