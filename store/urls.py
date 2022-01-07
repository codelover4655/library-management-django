from store.views import *
from django.urls import path

 
urlpatterns = [

    path('', index, name="index"),   
    path('books/', bookListView, name="book-list"),    
    path('book/<int:bid>/', bookDetailView, name='book-detail' ),
    path('books/loaned/', viewLoanedBooks, name="view-loaned"),
    path('books/loan/', loanBookView, name="loan-book"),
    path('book/form/<int:id>/', loneform, name="loneform"),
    path('books/return/', returnBookView, name="return-book"),
    path('books/ratebyuser/',ratebyUserView, name="rate-book"),
    

    




]

