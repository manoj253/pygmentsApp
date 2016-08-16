from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.http import HttpResponseRedirect,HttpResponse,Http404
from .forms import UserLoginForm,UserRegisterForm
from snippets.forms import SnippetForm
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from snippets.models import Snippet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change




def index(request):
	return render(request,'snippets/index.html')

def login_view(request):
	title = "Login"
	
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		login(request,user)
		
		return redirect("/")
	context = {
		"title":title,
		"form":form,
	}


	return render(request,"snippets/form.html",context)



def register_view(request):
	
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username,password=password)
		login(request,new_user)
		return redirect('/login/')
		#redirect
	context = {
		"title":title,
		"form": form,
	}

	return render(request,"snippets/form.html",context)


def logout_view(request):
	title = "Logout"
	logout(request)
	context = {"title":title}
	
	return render(request,"snippets/logout.html",{})


@login_required(login_url="/login/")

def createSnippet(request):
	
	if not request.user.is_authenticated():
		raise Http404
	title = "Snippet"
	if request.method=='POST':
		form = SnippetForm(request.POST)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.user = request.user
			instance.save()
			
			return HttpResponseRedirect(instance.get_absolute_url())

	else:
		form = SnippetForm()
	context = {
		"title":title,
		"form":form,
	}
	return render(request,'snippets/createSnippet.html',context)

def pygView(request,pk):
	obj = Snippet.objects.get(pk=pk)
	return render(request,'snippets/pygView1.html',{"obj":obj})

def pyg_list(request):
	queryset = Snippet.objects.all()
	context = {
		'object_list':queryset,

	}
	return render(request,'snippets/list.html',context)

def pyg_edit(request,pk):
	obj = get_object_or_404(Snippet,pk=pk)
	if not request.user.is_authenticated():
		raise Http404
	title = "Snippet"
	if request.method=='POST':
		form = SnippetForm(request.POST,instance=obj)
		if form.is_valid():
			instance=form.save(commit=False)
			instance.user = request.user
			instance.save()
			
			return HttpResponseRedirect(instance.get_absolute_url())

	else:
		form = SnippetForm(instance=obj)
	context = {
		"title":title,
		"form":form,
	}
	return render(request,'snippets/createSnippet.html',context)





