from django import forms
from django.contrib import admin
from .models import Books,Borrowed_books
from datetime import datetime
from django.contrib.auth.models import User
# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ("title","author","copy_number","subject_area","publication_date","status")
    list_filter = ("subject_area","status")
    search_fields = ("title","author")
admin.site.register(Books,BooksAdmin)

class BorrowedBookChoicesField(forms.ModelChoiceField):

    def label_from_instance(self, obj) -> str:
        return f"{obj.title}"

class BorrowedBooksAdmin(admin.ModelAdmin):
    list_display = ("book_name", "pickup_date", "return_date", "fine_charged", "return_status", "student")
    list_filter = ("book","user")
    def book_name(self, obj):
        return Books.objects.get(id=obj.book_id).title

    def fine_charged(self, obj):
        return f"ugx: {obj.fine:,}"

    def student(self, obj):
        student = User.objects.get(id=obj.user_id)
        return f"{student.first_name} {student.last_name}"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'book':
            return BorrowedBookChoicesField(queryset=Books.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change) -> None:

        if change:
            return_date = datetime.strftime(obj.return_date, "%Y-%m-%d %H:%M:%S:%f")
            fine = 0
            late_return = datetime.utcnow() - datetime.strptime(return_date, "%Y-%m-%d %H:%M:%S:%f")
            if late_return.days >= 3 and late_return.days < 10:
                fine = 5000
            elif late_return.days >= 10:
                fine = 15000

            obj.fine = fine

        return super().save_model(request, obj, form, change)

admin.site.register(Borrowed_books, BorrowedBooksAdmin)