from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from library.models import Book, User_info, Book_record
from library.forms import ContactForm
from django.contrib import auth, messages
from django.template import RequestContext
from django.core.context_processors import csrf
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from django.db import transaction, IntegrityError

ACTIVE = 'submit'
INACTIVE = 'button'

def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        elif len(q) > 20:
            error = True
        else:
            books = Book.objects.filter(title__contains=q)
            return render_to_response('search_results.html',
                {'books': books, 'query': q})
    return render_to_response('search_form.html',
        {'error': error})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #send_mail(
            #    cd['subject'],
            #    cd['message'],
            #    cd.get('email', 'noreply@example.com'),
            #    ['siteowner@example.com'],
            #)
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
	initial={'subject': 'I love your site!'}
    return render_to_response('contact_form.html', {'form': form})

#def home(request):
#   return render_to_response('index0.html')

def guide(request):
    #now = datetime.datetime.now()
    return render_to_response('guide.html')

def home(request):
    books_list = Book.objects.filter(title__contains = 'Data').order_by('title')
    return render_to_response('index1.html', {'books_list': books_list})

def user_info(request):
    if request.user.is_authenticated():
	user_dict = {'user_name': request.user.username, 'logged_in': True}	
    else:
	user_dict = {'user_name': '', 'logged_in': False}
    return user_dict

def go_index(request):
    books_list1 = Book.objects.order_by('-lend_time')[0: 3]
    books_list2 = Book.objects.order_by('-publish_date')[0: 3]
    user_dict = user_info(request)
    return render_to_response('index2.html', 
	{'books_list1': books_list1, 'books_list2': books_list2, 'user_name': user_dict['user_name'], 'logged_in': user_dict['logged_in']})

def book_filter(original_list, filter_list, request):
    filtered_list = Book.objects.filter(title='')
    check_list = []
    all_null = True
    for filt in filter_list:
        filter_cond = request.GET[filt]
        if (filter_cond != 'null'):
	     check_list = check_list + ['checked="checked"'];
	     all_null = False
	else:
	     check_list = check_list + [' '];
        filtered_list = filtered_list | original_list.filter(catagory = filter_cond)
    return [filtered_list, check_list, all_null]

def book_range(original_list, filter_list, request):
    filtered_list = Book.objects.filter(title='')
    check_list = [] 
    all_null = True
    for filt in filter_list:
        filter_cond = request.GET[filt]
        if filter_cond == 'null':
	     check_list = check_list + [' '];
	elif filter_cond == 'Earlier':
	     check_list = check_list + ['checked="checked"'];
	     start_date = date(1970, 1, 1)
	     end_date = date(2003, 12, 31)
             filtered_list = filtered_list | original_list.filter(publish_date__range=(start_date, end_date))
	     all_null = False
	else:
	     check_list = check_list + ['checked="checked"'];
	     start_date = date(int(filter_cond), 1, 1)
	     end_date = date(int(filter_cond), 12, 31)
             filtered_list = filtered_list | original_list.filter(publish_date__range=(start_date, end_date))
	     all_null = False

    return [filtered_list, check_list, all_null]

def book_order(original_list, filter_list, request):
    check_list = [''] * 5
    all_null = True
    for filt in filter_list:
	filter_cond = request.GET[filt]
	if filter_cond != 'null':
	     all_null = False
             break
    if all_null:
	filter_cond = 'title'
	filtered_list = original_list.order_by(filter_cond)
	check_list[0] = 'checked="checked"'
    else:
	check_list[filter_list.index(filt)] = 'checked="checked"'
	filtered_list = original_list.order_by(filter_cond)

    return [filtered_list, check_list, filter_cond]

def search_book(request):
    check_list = [' '] * 21
    books_list = Book.objects.filter(title='')
    q = 'search'
    key = 'null'
    message = ''
    user_dict = user_info(request)
    if 'submit' in request.GET:
	submit = request.GET['submit']
	if 's' in request.GET:
		q = request.GET['s']
    	else:
		message = 'No request!'
	if q != '':
		books_list = Book.objects.filter(title__contains=q).order_by('title')
	else:
		q = 'search'
    	if submit == 'jump':
        	query = q
    	elif submit == 'current':
        	filter_list = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']
		[books_cata, check_list1, all_null] = book_filter(books_list, filter_list, request)
		if all_null:
		      books_cata = books_list
		filter_list = ['c10', 'c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21']
		[books_date, check_list2, all_null] = book_range(books_cata, filter_list, request)
		if all_null:
		      books_date = books_cata
        	filter_list = ['c22', 'c23', 'c24', 'c25', 'c26']
		[books_order, check_list3, key] = book_order(books_date, filter_list, request)
		check_list = check_list1 + check_list2 + check_list3
		books_list = books_order
    	else:
		message = 'No other!'
    else:
	error = True
	message = 'No submit!'
    count = books_list.count()
    books_lists = ['']*(count/3+1)
    for i in range(0, count/3):
	three_books = [books_list[3*i], books_list[3*i+1], books_list[3*i+2]]
	books_lists[i] = three_books
    if count % 3 == 1:
	books_lists[count/3] = [books_list[count-1], [], []]
    elif count % 3 == 2:
	books_lists[count/3] = [books_list[count-2], books_list[count-1], []]
    #a = a+1
    return render_to_response('browse.html', 
		{'message': message, 'books_lists': books_lists, 'query': q, 'count': count, 'check_list': check_list, 'user_name': user_dict['user_name'], 'logged_in': user_dict['logged_in'], 'key': key})

def get_button(isbn, usr):
    global ACTIVE, INACTIVE
    the_book = Book.objects.get(ISBN = isbn)
    the_records = usr.mybooks.all()
    button_style = {'borrow': ACTIVE, 'return': ACTIVE}
    if the_book.inventory <= 0:
	button_style['borrow'] = INACTIVE
    try:
        a_rec = the_records.get(book_ISBN = isbn)
	button_style['borrow'] = INACTIVE
    except ObjectDoesNotExist:
	button_style['return'] = INACTIVE
    return button_style

@transaction.atomic
def book_info(request):
    button = {'borrow': ACTIVE, 'return': ACTIVE}
    global ACTIVE, INACTIVE
    user_dict = user_info(request)
    if 'i' in request.GET:
        isbn = request.GET['i']
        if not isbn:
            error = '404'
        else:
            try:
		a_book = Book.objects.get(ISBN = isbn)
	    except Book.DoesNotExist:
		error = '404'
	    else:
		error = ''
    elif 'info' in request.GET:
    	if not request.user.is_authenticated():
	    return HttpResponseRedirect('/home/login/')
   	a_user = User_info.objects.get(username = request.user.username)
	#action = request.GET['return_info']
	isbn = request.GET['info']
	a_book = Book.objects.get(ISBN = isbn)
	error = ''
	if 'borrow_info' in request.GET:
	    return_date = date.today()
	    return_date = return_date.replace(month=return_date.month+3)
	    a_record = Book_record.objects.create(book_ISBN = isbn, book_title = a_book.title, return_date = return_date)
	    a_user.mybooks.add(a_record)
	    Book.objects.filter(ISBN = isbn).update(inventory = a_book.inventory-1, lend_time = a_book.inventory+1)
	if 'return_info' in request.GET:
	    records = a_user.mybooks.all()
	    a_record = records.get(book_ISBN = isbn)
	    a_user.mybooks.remove(a_record)
	    Book.objects.filter(ISBN = isbn).update(inventory = a_book.inventory+1, lend_time = a_book.inventory+1)	
            #button = get_button(isbn, a_user)
    else:
        error = '404'
    if error == '404':
	return HttpResponseRedirect('/home/404/')
    else:
	if request.user.is_authenticated():
		a_user = User_info.objects.get(username = request.user.username)
		button = get_button(isbn, a_user)
	a_book = Book.objects.get(ISBN = isbn)
        return render_to_response('book_info.html',
            {'error': error, 'book': a_book, 'user_name': user_dict['user_name'], 'logged_in': user_dict['logged_in'],
             'borrow_button': button['borrow'], 'return_button': button['return']})
  

def login_view(request):
    user_dict = user_info(request)
    message = ''
    if request.POST:
          username = request.POST.get('username')
          password = request.POST.get('password')
	  user = auth.authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  auth.login(request, user)
                  #request.session['admin_id'] = user.id
                  #return render_to_response('home/index2.html',  context_instance = RequestContext(request))
                  return HttpResponseRedirect('/home/mybooks/')
	      else:
                  # do something because user was not active
                  #messages.add_message(request, messages.ERROR, 'User Inactive')
		  message = "There was an error with your E-Mail/Password combination. Please try again."
          else:
               # password/username combination was wrong
               message = "There was an error with your E-Mail/Password combination. Please try again."
	       #messages.add_message(request, messages.ERROR, 'Invalid Credentials')

    return render(request, 'logon.html', {'message': message, 'user_name': user_dict['user_name'], 'logged_in': user_dict['logged_in']})

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/home/index2/')

def get_info(request, target):
    I_get = request.POST.get(target)
    if I_get == target or I_get == '':
	 return 'none'
    else:
	 return I_get

def register_view(request):  
    user_dict = user_info(request)
    if request.POST:
            username = get_info(request, 'Username')
            password = get_info(request, 'Password')
	    if User.objects.filter(username = username).exists():
		return render(request, 'reg.html', 
			{'error': 'The username has been registered. Please try again.'})
	    else:
		email = get_info(request, 'Email')
		user = User.objects.create_user(username = username, email = email, password = password)
		try:
			user.save()
		except IntegrityError:
			transaction.rollback()
		User_info.objects.create(	
			username = username,
			email = email,
			country = get_info(request, 'Country'),
			city = get_info(request, 'City'),
			code = get_info(request, 'Code'),
			number = get_info(request, 'Number'),
			address = get_info(request, 'Address'),
			company = get_info(request, 'Company'),
		)
	    	new_user = auth.authenticate(username=username, password=password)
		auth.login(request, new_user)
	    	return HttpResponseRedirect('/home/index2/')
    else:
	 return render(request, 'reg.html', 
			{'user_name': user_dict['user_name'], 'logged_in': user_dict['logged_in']})

def mybooks_view(request):
    if not request.user.is_authenticated():
	return HttpResponseRedirect('/home/login/')
    user_dict = user_info(request)
    user_name = request.user.username
    a_user = User_info.objects.get(username = user_name)
    books_record = a_user.mybooks.all()
    return render_to_response('mybooks.html', 
		{'count': books_record.count(), 'books_record': books_record, 'user_name': user_dict['user_name'], 'logged_in': user_dict['logged_in']})
	

# Create your views here.
