import email
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from .models import Books, Borrowed_books
from datetime import datetime
from django.core.mail import send_mail




# Create your views here.
def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect(request.build_absolute_uri('/lib/books'))
        
        messages.info(request,'invalid username or password')
        return redirect(request.build_absolute_uri('/lib/login'))
    # if request is GET
    else: 
        return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        last_name =  request.POST['last_name']
        if password1!=password2:
            messages.info(request,'Password not matching') 
            return redirect(request.build_absolute_uri('/lib/register'))
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username taken')
            return redirect(request.build_absolute_uri('/lib/register'))
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email taken')
            return redirect(request.build_absolute_uri('/lib/register'))
        else:
            user = User.objects.create_user(
                username=username,email=email,
                password=password1,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('/')
            # add message
        
              
        
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
    user=user,pickup_date=datetime.now(),fine=0)
    borrowed_book.save()

    

    return redirect(request.build_absolute_uri('/lib/my/books'))


def student_borrowed_books(request):
    
    books = Borrowed_books.objects.filter(user_id=request.user.id).select_related()
    #select_related fetches other details about the book
        
    return render(request,'hope/borrowed_books.html',{
        'books': books,
        'categories':books_categories() ,
        'title': 'My Borrow Book'
    })



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

def unpicked_booked_books():
    """
     Unpicked Books
    """
    #fetch all unpicked books
    books = Borrowed_books.objects.filter(return_status='BK')
    
    #if the books objects is empty, return response
    if not books.count():
        return 0 # return an http response
    else: 
        #looping through the returned objects(books)
        updated_books = 0

        for book in books:
            # strftime converts datetime object to string
            diff = datetime.now() - datetime.strptime(datetime.strftime(book.pickup_date,"%Y-%m-%d %H:%M:%S:%f"),"%Y-%m-%d %H:%M:%S:%f")

            #check the diffence in minutes
            if diff.total_seconds()/60 > 60:
                 #call the 2nd function to make a book available
                update_books_availability(book_id=book.book_id)
                # call the 3rd function to the delete the related record from borrowed books
                delete_unpicked_booked_books(book_id=book.id)
                updated_books += 1
                #book_id = id where id is the primary key for the books...or the id of that specific book
        return updated_books

def unpicked(request):
    unpicked_books = unpicked_booked_books()
    mss = "No unpicked books available"
    if unpicked_books:
        mss = f"{unpicked_books} have been made available for booking"
    
    messages.info(request, mss)

    return render(request,'unpicked.html', {"categories": books_categories()})


def send_notification(request):
    if request.method == "POST":
        sub = request.POST.get('subject')
        msg = request.POST.get('message')
        e_mail = request.POST.get('e_mail')
        
        send_mail(
            sub,msg,'aina.isaac@gmail.com',[e_mail]
        )
        return HttpResponse('Email sent')
    return render(request,'notification.html')