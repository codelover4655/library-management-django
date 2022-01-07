
from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .myforms import user_form
from  django import forms

# Create your views here.

def index(request):
    print(request.user)
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    obj=get_object_or_404(Book,id=bid)
    str=obj.title
    x=BookCopy.objects.filter(book__title=str,status=True)
    context = {
        'book': obj, # set this to an instance of the required book
        'num_available': x.count, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    return render(request, template_name, context=context)


@csrf_exempt      # yet   to explore this command 
def bookListView(request):
    print(request.user)
    template_name = 'store/book_list.html'
    obj =Book.objects.all()
    print(obj[0].author)
    context = {
        'books': obj,      
          # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }

    return render(request, template_name, context=context)







@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    y=get_object_or_404(User,id=request.user.id)
    x=BookCopy.objects.filter(borrower=y)
    context = {
        'books': x,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''

    return render(request, template_name, context=context)











@csrf_exempt
@login_required
def loanBookView(request):

    book_id =request.POST.get('bid')
    
    obj=get_object_or_404(Book,id=book_id)
    x=BookCopy.objects.filter(book__title=obj.title,status=True)
    y=x.count()
    
    if y!=0 :
        response_data = {
        'message': 'success',
        'id':  book_id,}
        z=x[0]
        #z.status=False
        z.save()
        yoyo=request.user       #for name of borrower

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 



@csrf_exempt
@login_required
def returnBookView(request):
    print(request.POST)
    print(request.POST)
    bid=request.POST['bid']
    x=get_object_or_404(BookCopy,id=bid)
    x.status=True
    x.borrow_date=None
    x.borrower=None
    x.save()


    response_data = {
        'message': 'success',}   
    return JsonResponse(response_data)
















@login_required
def loneform(request,id):
    form=user_form()
    template_name = 'store/create_lone_form.html'
    if(request.method == 'POST'):

        form=user_form(request.POST)
        if form.is_valid():

            y=request.POST.get('borrower')
            #print(y)
            y1=request.POST['book']
            y2=get_object_or_404(Book,id=y1)
            y3=y2.title
            x=BookCopy.objects.filter(book__title=y3,status=True) 
            print(x)
            if(x.count()!=0):
                z=x[0]
                z.status=False
                z1=get_object_or_404(User,id=y)
                #print(z1)
                z.borrower=z1
                z.borrow_date=request.POST['borrow_date'] 
                z.save()      
                print('done ')

            else:
                raise forms.ValidationError(('you can issue it please wait for someone to return it '), code='invalid')
                

            return redirect('../../../')

        else: 
            raise forms.ValidationError(('Invalid value'), code='invalid')

    
    return render(request, template_name, {'obj': form})





@csrf_exempt
@login_required 
def ratebyUserView(request):
    
    
    user_id=request.user.id
    user_obj=get_object_or_404(User, id=user_id)
    book_id=request.POST['bid']
    book_obj=get_object_or_404(Book, id=book_id)
    new_rating=request.POST['rating']
    print(new_rating)
    x=Userrating.objects.filter(user=user_obj,book=book_obj)
    if x.count()==0 :
        y=Userrating(user=user_obj,book=book_obj,ratingbyuser=new_rating)
        y.save()
    else :
        z=x[0]
        z.ratingbyuser=new_rating
        z.save()

    y=Userrating.objects.filter(book=book_obj)
    rt=0
    rtr=0
    for a in y:
        rt+=a.ratingbyuser
        rtr+=1
    rt=rt/rtr
    book_obj.rating=rt
    book_obj.save()
    
    response_data = {
        'message': 'success',}   
    return JsonResponse(response_data)




        

         



    


 
    
