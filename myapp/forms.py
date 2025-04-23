from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Albumin, Profile, UserSettings, JsonData, Book, BookFile

# Get the custom user model
User = get_user_model()

# Albumin Form
class AlbuminForm(forms.ModelForm):
    class Meta:
        model = Albumin
        fields = ['title', 'description', 'sub_title', 'sub_content', 'image', 'category', 'youtube_video']
        widgets = {
            'sub_content': forms.Textarea(attrs={'rows': 3, 'cols': 20}),
        }

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'profile_picture', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if self.cleaned_data.get('profile_picture'):
                profile.profile_picture = self.cleaned_data['profile_picture']
                profile.save()
        return user

# User Settings Form
class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['date', 'time', 'timezone', 'language', 'feedback']

# File Upload Form (Single File)
class UploadFileForm(forms.Form):
    file = forms.FileField()

# JSON Data Form
class JsonDataForm(forms.ModelForm):
    class Meta:
        model = JsonData
        fields = ['title', 'category', 'description', 'sub_title', 'subtitle_content']

# Book Form
# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ['title', 'description', 'category', 'image']

# # Book File Upload Form (Single File)
# class BookFileUploadForm(forms.ModelForm):
#     file = forms.FileField(widget=forms.ClearableFileInput(), required=True)

#     class Meta:
#         model = BookFile
#         fields = ['file']

# Multiple File Upload Form
class MultipleBookFileUploadForm(forms.Form):
    def save_files(self):
        uploaded_files = self.files.getlist('files')  # Get the list of uploaded files
        book_files = []
        for file in uploaded_files:
            book_file = BookFile(file=file)  # Assuming you have a BookFile model
            book_file.save()
            book_files.append(book_file)
        return book_files


# class MultipleBookFileUploadForm(forms.Form):
#     files = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={'multiple': True}),
#         required=True
#     )
    # You can customize the form field for subtitle_content here if needed.
    # subtitle_content = forms.CharField(widget=forms.Textarea, required=False)

# from django import forms
# from .models import BookFile

# class BookFileForm(forms.ModelForm):
#     files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)

#     class Meta:
#         model = BookFile
#         fields = ['title', 'description', 'category', 'files']

#     def save(self, commit=True):
#         uploaded_files = self.files.getlist('files')
#         book_files = []
#         for file in uploaded_files:
#             book_file = BookFile(title=self.cleaned_data['title'],
#                                  description=self.cleaned_data['description'],
#                                  category=self.cleaned_data['category'],
#                                  file=file)
#             if commit:
#                 book_file.save()
#             book_files.append(book_file)
#         return book_files

from django import forms

class SequenceForm(forms.Form):
    sequence = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter DNA, RNA, or Protein sequence...'}),
        label="Sequence Input",
        required=True
    )
