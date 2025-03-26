"""
URL configuration for Myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name="home"),
    path('Databases/<int:id>/', views.Databases, name="Databases_detail"),
    path('category/', views.search_category, name="search_category"),
    path('signin/', views.sign_in, name='signin'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name="profile"),
    path('settings/', views.setting, name="settings"),
    path("update-password/", views.update_password, name="update_password"),
    path('save-settings/', views.save_settings, name="save_settings"),
    path('submit-feedback/', views.submit_feedback, name="submit_feedback"),  # New feedback URL
    path('navbar/', views.navbar, name="navbar"),

    # Json Files Uploads:
    path('uploads/', views.upload_json, name='upload_json'),
    path('json-detail/<int:id>/', views.json_detail, name='json_detail'),
    path('json/edit/<int:id>/', views.json_edit, name='json_edit'),
    path('json/delete/<int:id>/', views.json_delete, name='json_delete'),

    path('Forms/', views.new_file, name="new_file"),
    path('submit/', views.form_view, name='submit_form'),
    path('update_protein/<int:id>/', views.update_protein, name="update_protein"),
    path('delete_protein/<int:id>/', views.delete_protein, name="delete_protein"),
    path('update_genome/<int:id>/', views.update_genome, name="update_genome"),
    path('delete_genome/<int:id>/', views.delete_genome, name="delete_genome"),
    path('update_nucleotide/<int:id>/', views.update_nucleotide, name="update_nucleotide"),
    path('delete_nucleotide/<int:id>/', views.delete_nucleotide, name="delete_nucleotide"),
    path('update_blast/<int:id>/', views.update_blast, name="update_blast"),
    path('delete_blast/<int:id>/', views.delete_blast, name="delete_blast"),
    path('update_pubchem/<int:id>/', views.update_pubchem, name="update_pubchem"),
    path('delete_pubchem/<int:id>/', views.delete_pubchem, name="delete_pubchem"),
    path('update_taxonomy/<int:id>/', views.update_taxonomy, name="update_taxonomy"),
    path('delete_taxonomy/<int:id>/', views.delete_taxonomy, name="delete_taxonomy"),

    ## Books
    path('books/', views.books, name='books'),
    path('upload-book/', views.upload_files, name='upload_files'),
    
    ##search
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('download/<str:book_name>/', views.download, name='download'),
    path('results/', views.results, name='results'),
    path('ajax/search_pdf/', views.search_pdf, name='search_pdf'),
    path('ajax/search_google/', views.search_google, name='search_google'),
    path('ajax/search_youtube/', views.search_youtube, name='search_youtube'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    