from operator import index
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'hope'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('books/',views.index,name='index'),
    # <str:category>, passing the parameter from the template
    path('books/category/<str:category>/list', views.books_by_category, name='books_by_category'),
    path('book/<int:id>/Borrow',views.Borrow,name='Borrowpage'),
    path('book/borrow', views.borrow_book, name='borrow_book'),
    path('my/books', views.student_borrowed_books, name="student_borrowed_books"),
    path('books/unpicked',views.unpicked_booked_books,name="unpicked_borrowed_books")
   
   
]

urlpatterns += staticfiles_urlpatterns()