from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    #parent_id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    content=forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'message','rows':2, 'cols':45}),label="")
    
    class Meta:
        model = Comment
        fields = [
            "content",
        ]