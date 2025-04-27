from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Constants for category choices
CATEGORY_CHOICES = [
    ('protein', 'Protein'),
    ('genome', 'Genome'),
    ('nucleotide', 'Nucleotide'),
    ('taxonomy', 'Taxonomy'),
    ('pubchem', 'Pubchem'),
    ('blast', 'Blast'),
    ('general', 'General'),
]

class Albumin(models.Model):
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    sub_title = models.CharField(max_length=250)
    sub_content = models.JSONField(blank=True, null=True)
    image = models.ImageField(upload_to='albumins/')
    youtube_video = models.URLField(blank=True, null=True)

    def get_embedded_youtube_url(self):
        if self.youtube_video and "watch?v=" in self.youtube_video:
            return self.youtube_video.replace("watch?v=", "embed/")
        return self.youtube_video  # Return as-is if already correct
    
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'datas'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['title']),
        ]
        verbose_name = 'Albumin'
        verbose_name_plural = 'Albumins'

    def __str__(self):
        return f"{self.title} - {self.category}"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

    
# date & time codes:
class UserSettings(models.Model):
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    timezone = models.CharField(max_length=50, default="UTC")
    language = models.CharField(max_length=10, default="en")
    feedback = models.TextField(null=True, blank=True)  # Use TextField for longer feedback

    def __str__(self):
        return f"{self.date} {self.time} - {self.timezone} - {self.language} - {self.feedback}"

class JsonData(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    subtitle_content = models.JSONField(blank=True, null=True)
    
    # File field for uploading files within the 'uploads' folder
    file_upload = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.title
    
## Books:
from django.core.files import File
from django.core.files.base import ContentFile
import os

from django.core.files import File
import os

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Protein', 'Protein'),
        ('Genome', 'Genome'),
        ('Nucleotide', 'Nucleotide'),
        ('Taxonomy', 'Taxonomy'),
        ('PubChem', 'PubChem'),
        ('BLAST', 'BLAST'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='covers/', blank=True, null=True, default='covers/default_book.png')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Protein')

    def save(self, *args, **kwargs):
        """Automatically extract cover image if not present"""
        super().save(*args, **kwargs)  # Save instance first to get the file path

        # Fetch the first related BookFile
        book_file = self.files.first()
        if book_file and book_file.file and (not self.image or self.image.name == "covers/default_book.png"):
            from myapp.views import extract_first_page_image
            image_path = extract_first_page_image(book_file.file.path)

            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    self.image.save(os.path.basename(image_path), File(img_file), save=True)

class BookFile(models.Model):
    book = models.ForeignKey(Book, related_name='files', on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(upload_to='books/')  
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.file.name


# ## Books:
# from django.conf import settings
# from django.db import models
# from urllib.parse import urljoin
# import os

# class Book(models.Model):
#     CATEGORY_CHOICES = [
#         ('Protein', 'Protein'),
#         ('Genome', 'Genome'),
#         ('Nucleotide', 'Nucleotide'),
#         ('Taxonomy', 'Taxonomy'),
#         ('PubChem', 'PubChem'),
#         ('BLAST', 'BLAST'),
#     ]
    
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     file = models.FileField(upload_to='books/')
#     image = models.ImageField(upload_to='covers/', blank=True, null=True, default='covers/default_book.png') 
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Protein')

#     def __str__(self):
#         return f"{self.title} ({self.category})"

#     def get_image_url(self):
#         """Ensure the correct image URL is stored and returned."""
#         if self.image:
#             return urljoin(settings.MEDIA_URL, self.image.name)
#         return urljoin(settings.MEDIA_URL, "covers/default_book.png")

from django.db import models

class SequenceAnalysis(models.Model):
    sequence = models.TextField()
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis on {self.created_at}"

class Proteins(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sequence = models.TextField()
    source = models.CharField(max_length=255, blank=True, null=True)  # Example: "NCBI", "UniProt"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name