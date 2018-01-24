from django import forms
from blog.models import Post, Comment

#create classes
class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author', 'title', 'text')
        #the following codes is used to setup classes for using CSS, such 'textinputclass'
        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})     
        }
class CommentForm(forms.ModelForm):
    class Meta():        
        model = Comment
        fields = ('author', 'text')
        #the following codes is used to setup classes for using CSS, such 'textinputclass'
        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}), #CSS class: textinputclass
            'text':forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }