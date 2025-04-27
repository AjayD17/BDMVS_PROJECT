from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import *

admin.site.register(Albumin)
admin.site.register(Profile)
admin.site.register(JsonData)
admin.site.register(UserSettings)
admin.site.register(Book)
admin.site.register(BookFile)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password', 'is_superuser')}),
    )
    list_filter = ('is_superuser',)  # Filter by superuser status

    def save_model(self, request, obj, form, change):
        if change:  # If user is being updated
            if 'password' in form.changed_data:
                obj.set_password(obj.password)  # Hash password correctly
        else:
            obj.password = make_password(obj.password)  # New user hashing

        super().save_model(request, obj, form, change)


from django.contrib import admin
from .models import Book, BookFile

class BookFileInline(admin.TabularInline):  
    model = BookFile
    extra = 1

class BookAdmin(admin.ModelAdmin):
    inlines = [BookFileInline]

# Register only once
admin.site.unregister(Book)  # ✅ Unregister first (to avoid duplicate registration)
admin.site.register(Book, BookAdmin)  # ✅ Register properly

