from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from .models import Books, Borrowed_books
from datetime import datetime



# Create your views here.
def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect(request.build_absolute_uri('/lib/books'))
        else:
            messages.info(request,'invalid username or password')
            return redirect(request.build_absolute_uri('/lib/login'))

    else:
        return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        student_number = request.POST['student_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number =  request.POST['phone_number']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect(reverse('register'))
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect(reverse('register'))
            else:
                user = User.objects.create_user(
                    username=username,email=email,
                    password=password1)
                user.save()
                return redirect('/')
        else:
            messages.info(request,'Password not matching') 
            return redirect(reverse('register'))   
        
    else:
        return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect(request.build_absolute_uri('/lib/login'))

def books_categories():
    """
        Get the categories of books
    """
    return Books.objects.only('category').distinct('category') 

def index(request):
    books = Books.objects.all().order_by('title')
    categories = books_categories() # call for categories
    return render(request,'hope/index.html',
        {'books':books, 'categories': categories, 'title': 'ALL Books'}
    )


def books_by_category(request, category):
    """
        View books for each category
    """
    # call for categories, used in the template navigation bar.
    categories = books_categories()
    books = Books.objects.filter(category=category)
    return render(request,'hope/books_by_category.html',
        {'books':books, 'categories': categories, 'title': f"Book in {category.upper()}"}
    )
    
def Borrow(request,id):
    book = Books.objects.get(id=id)
    
    categories = books_categories()

    return render(request,'hope/borrow_book.html',{
        'book': book,
        'categories': categories,
        'book_id': id,
        'title': 'Borrow a Book'
    })

def borrow_book(request):
   
    if request.method != "POST":
        return HttpResponseBadRequest({'message': 'Bad Request'})
    
    # get user id
    user_id = request.user.id
    book = Books.objects.get(id=request.POST.get('book_id'))
    if book.status == 'AV':
        book.status = 'UNAV'
        book.save()
    book_id = request.POST.get('book_id')
    book = Books.objects.get(id=book_id)
    user = User.objects.get(id=user_id) 

    borrowed_book = Borrowed_books.objects.create(book=book,
    user=user,fine=0)
    borrowed_book.save()

    return redirect(reverse('student_borrowed_books'))


def student_borrowed_books(request):
    
    books = Borrowed_books.objects.filter(user_id=request.user.id).select_related()
        
    categories = books_categories()

    return render(request,'hope/borrowed_books.html',{
        'books': books,
        'categories': categories,
        'title': 'My Borrow Book'
    })

# I have started with the 2nd and 3rd functions because i needed to call them in the 1st and am 
# not sure if it would have worked fine if i called a function i havent defined like before the
# first function.

def update_books_availability(book_id):
    """
        Make a book available for booking.
    """
    book = Books.objects.get(id=book_id)
    # make a book available for booking
    book.status = 'AV'
    book.save()

def delete_unpicked_booked_books(book_id):
    """
        Delete Unpicked Books From Borrowed Books records
    """
    # get unpicked book after the grace period
    book = Borrowed_books.objects.filter(id=book_id)
    # delete the record since book was never picked
    book.delete()

def unpicked_booked_books(request):
    """
     Unpicked Books
    """
    #fetch all unpicked books
    books = Borrowed_books.objects.filter(return_status='BK',pickup_date__icontains=datetime.today())
    #if the books objects is empty, return response
    if not books.count():
        return JsonResponse({"message": "No pending pickups"}) # return an http response
    else: 
        #looping through the returned objects(books)
        updated_books = 0

        for book in books:
            diff = datetime.now() - datetime.strptime(book.pickup_date,"%Y-%m-%d %H:%M:%S:%f")

            #check the diffence in minutes
            if diff.min > 60:
                 #call the 2nd function to make a book available
                update_books_availability(book_id=book.book_id)
                # call the 3rd function to the delete the related record from borrowed books
                delete_unpicked_booked_books(book_id=book.id)
                updated_books += 1
                #book_id = id where id is the primary key for the books...or the id of that specific book
        return JsonResponse(
            {"message": f"{updated_books} books made available for booking"})

