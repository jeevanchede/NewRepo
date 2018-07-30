# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import User,Books,Issue_Table,Return_Table,Book_history_ReturnedBooks
from django.shortcuts import render,redirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
#import datetime
from datetime import datetime, timedelta
from datetime import date
from reportlab.pdfgen import canvas
from django.http import HttpResponse
# Create your views here.

# def register(request):
# 	#check username if already exists
# 	return render(request,"register.html",{})

@csrf_exempt
def validations_register(request):
	context={}
	#context["msg"]
	if request.method == "GET":
		return render(request,"register.html",{})
	else :	
		nm=request.POST['nm']
		username=request.POST['un']
		password=request.POST['pass']
		email=request.POST['email']
		phone=request.POST['ph']
		typeuser=request.POST['tu']
		
		if User.objects.filter(username=username).exists():
			print "already exists"
			return redirect('/register/')
			#return redirect('/login/')
		else :
			aaa=User(name=nm,username=username,
				 password=password,
				 email=email,
				 phone_number=phone, 
				 typeuser=typeuser
				 	)
			aaa.save()
			print typeuser
		return redirect('/login/')	
		
# def login(request):
# 	return render(request,"login.html",{})
@csrf_exempt
def afterlogin(request):
	#if username exists and password matches
	#check usertye and redirect accordingly
	#if request.session.has_key["username"]:
	if "username" in request.session :
		tu = request.session['typeuser']
		if tu == "student":
			return redirect('/student_dashboard/')
		else:
			return redirect('/librarian_dashboard/')				

	if request.method == "GET":
		return render(request,"login.html",{})
	else :	
		user=request.POST['un']
		pas=request.POST['pass']
		if User.objects.filter(username=user).exists():
			user_obj=User.objects.get(username=user)
			if user_obj.password == pas :
				request.session["username"] = user
				request.session["typeuser"] =user_obj.typeuser
				print "logged in "+user_obj.typeuser
				if user_obj.typeuser == "student":
					return redirect('/student_dashboard/')
				else:
					return redirect('/librarian_dashboard/')		
			else:
				print "wrong password"
				return redirect('/login/')	
		else:	
			print "User doesn't exist"
			return redirect('/login/')

@csrf_exempt
def studentdash(request):
	if  "username" not in request.session:
		return redirect("/login/")
	elif request.session['typeuser'] != "student":
		return redirect("/login/")
		
	obj=list(Books.objects.all())
	context={}
	context['m']=obj
	return render(request,"student_dashboard.html",context)

@csrf_exempt	
def librariandash(request):
	if  "username" not in request.session:
		return redirect("/login/")
	elif request.session['typeuser'] != "librarian":
		return redirect("/login/")
	obj1=list(Issue_Table.objects.all())
	context={}
	obj2=list(Return_Table.objects.all())
	#obj2.order_by('return_date')
	obj3=sorted(obj2,key=lambda x:x.return_date)
	#obj2.sort(key=)
	context['m']=obj1
	context['n']=obj3
	

	return render(request,"librarian_dashboard.html",context)	
	

@csrf_exempt	
def logout(request):
	if "username" in request.session:
		del request.session['username']
	return redirect('/login/')

@csrf_exempt	
def book_details(request):
	context={}

	id=request.GET["book_id"]
	user_obj=Books.objects.get(id=id)
	context["m"]=user_obj.summary
	context["nm"]=user_obj.name
	context["auth"]=user_obj.author
	context["copies"]=user_obj.no_of_copies
	context["bid"]=id

	return render(request,"summary.html",context)

@csrf_exempt
def student_profile(request):
	context={}
	# if 'username' in request.session:
	# 	usrnm = request.session['username']
	 		# 	return render(request,'student_profile.html',context)
	# else:
	# 	return redirect('/login/')	
	if  "username" not in request.session:
		return redirect("/login/")
	elif request.session['typeuser'] != "student":
		return redirect("/login/")
	usrnm = request.session['username']
	user_obj = list(User.objects.filter(username=usrnm))
	context['m']=user_obj
	return render(request,'student_profile.html',context)

@csrf_exempt
def search(request):
	context={}
	if  "username" not in request.session:
		return redirect("/login/")
	elif request.session['typeuser'] != "student":
		return redirect("/login/")
	book = request.POST['name']
	#author = request.POST['author']
	#print book

	name_obj=list(Books.objects.filter(name=book))
	author_obj=list(Books.objects.filter(author=book))
	context['k']=Books.objects.filter(Q(name=book) | Q(author=book))
	context['n']=name_obj
	context['a']=author_obj
	return render(request,"search_book.html",context)				
	
@csrf_exempt
def abcd(request):
	if  "username" not in request.session:
		return redirect("/login/")
	else :
		if request.session['typeuser'] == "student":
			return redirect("/student_dashboard/")
		else:
			return redirect("/librarian_dashboard/")

		
@csrf_exempt
def status(request):
	context={}
	id=request.GET["book_id"]
	usernm=request.session["username"]
	user_obj=User.objects.get(username=usernm)
	book_obj=Books.objects.get(id=id)
	#issued_books=Return_Table.objects.get(student_name=usernm)
	if book_obj.no_of_copies == 0:
		context["msg"]="Sorry no copies left"
	elif 	Return_Table.objects.filter(student_name=usernm).exists():
		context["msg"]="already have a book"
	else:
		user_name = user_obj.username
		#already_booked = Issue_Table.objects.get(student_name=user_name)
		if Issue_Table.objects.filter(student_name=user_name).exists():
			context["msg"]="You have not returned previous book"
			return render(request,"status.html",context)		

		#print already_booked
		obj=Issue_Table(Book_name=book_obj.name,student_name=user_obj.username,status="Booked",issue_date=date.today(),return_date=(date.today() + timedelta(days=7)))
		obj.save()
		print book_obj.no_of_copies
		book_obj.no_of_copies-=1
		print book_obj.no_of_copies
		book_obj.save()
	 	context["msg"]="Successfully booked"

	return render(request,"status.html",context)		


@csrf_exempt
def pickedup(request):
	status=request.GET["status"]
	username=request.GET["username"]
	book_name=request.GET["bookname"]
	if status == "picked up":
		user_obj=Issue_Table.objects.get(student_name=username,Book_name=book_name )
		user_obj.status="Issued"
		user_obj.save()
		return_obj=Return_Table(Book_name=user_obj.Book_name,student_name=user_obj.student_name,status=user_obj.status,issue_date=user_obj.issue_date,return_date=user_obj.return_date)
		return_obj.save();
		user_obj.delete()
	return redirect("/librarian_dashboard/")

@csrf_exempt
def returned(request):
	username=request.GET["username"]
	book_name=request.GET["bookname"]
	user_obj=Return_Table.objects.get(student_name=username,Book_name=book_name )
	#user_obj.status="Returned"
	#user_obj.save()
	book_obj=Books.objects.get(name=book_name)
	book_obj.no_of_copies+=1
	book_obj.save()
	return_obj=Book_history_ReturnedBooks(Book_name=user_obj.Book_name,student_name=username,issue_date=user_obj.issue_date,return_date=user_obj.return_date)
	return_obj.save();	
	user_obj.delete()
	late_days=(datetime.now().date()-user_obj.return_date).days
	print late_days
	late_fee=late_days*50
	
	if late_days < 0:
		print "ok"
	else:
		return redirect("/pdf/?late_fee="+str(late_fee))

	#user_obj.delete()
	return redirect("/librarian_dashboard/")


def gen_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    print "in pdf"
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    lf=request.GET["late_fee"]
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    s="Fee is:"+str(lf)
    p.drawString(100, 100, s)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    #return redirect("/librarian_dashboard/")
    return response


def base(request):
	return render(request,"base.html",{})


def issued_books(request):
	user=request.session["username"]
	data=Return_Table.objects.filter(student_name=user)
	context={}
	context['m']=data
	print "Here"
	return render(request,"issued.html",context)



def returned_books(request):
	user=request.session["username"]
	data=Book_history_ReturnedBooks.objects.filter(student_name=user)
	context={}
	context['n']=data
	return render(request,"returned.html",context)


