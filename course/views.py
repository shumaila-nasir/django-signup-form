from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, EditForm, EditAdminForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# signup view func
def sign_up(request):

	if request.method == 'POST':
		fm = SignUpForm(request.POST)
		if fm.is_valid():
			print('save')
			messages.success(request, 'Your was created successfully !!')
			fm.save()

	else:
		fm = SignUpForm()
		print('not save')
	return render(request, 'register.html', {'form':fm})


# login view func

def user_login(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			fm = AuthenticationForm(request=request, data=request.POST)
			print('login')
			if fm.is_valid():
				uname = fm.cleaned_data['username']
				upass = fm.cleaned_data['password']
				user = authenticate(username=uname, password=upass)
				if user is not None:

					login(request, user)
					messages.success(request, 'login Succeccfully!!')
					return redirect('/profile/')

		else:
			fm =AuthenticationForm()
			print("not login")
		return render(request, 'login.html', {'form': fm})
	else:
		return redirect('/profile/')
# profile func

def user_profile(request):
	if request.user.is_authenticated:
		print('authenticate')
		if request.method == 'POST':
			if request.user.is_superuser == True:
				fm = EditAdminForm(request.POST, instance=request.user)
				users = User.objects.all()
			else:
				fm = EditForm(request.POST, instance=request.user)
				users = None
			if fm.is_valid():
				print('valid')
				messages.success(request, ' Update Successfully!!!')
				fm.save()
		else:
			if request.user.is_superuser == True:
				fm = EditAdminForm(instance=request.user)
				users = User.objects.all()
			else:
				fm = EditForm(instance=request.user)
				users = None
		return render(request, 'profile.html', {'name': request.user.username, 'form': fm, 'users': users})
	else:
		return redirect('/login/')

# Logout

def user_logout(request):
	logout(request)
	return redirect('/login/')

# change password with old password
@login_required(login_url= '/login/')
def change_pass(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			fm = PasswordChangeForm(user=request.user, data=request.POST)
			if fm.is_valid():
				fm.save()
				update_session_auth_hash(request, fm.user)
				messages.success(request, 'Password Change successfully')
				return redirect('/profile/')
		else:
			fm = PasswordChangeForm(user=request.user)
		return render(request, 'changepass.html', {'form': fm})
	else:
		return redirect('/login/')

def user_details(request, id):
	if request.user.is_authenticated:
		pi = User.objects.get(pk=id)
		fm = EditAdminForm(instance=pi)

		return render(request, 'userdetails.html', {'form':fm})
	else:
		return redirect('/login/')
