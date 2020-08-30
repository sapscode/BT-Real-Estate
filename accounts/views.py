from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
#from contacts.models import Contact

def register(request):
    if request.method == 'POST':
        #getting all the values from the request
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Check if passwords match 
        if password == password2:
            #Check username
            if User.objects.filter(username=username).exists(): #username=username, checking if any username attribute in the database matches with the current passed username
                messages.error(request, 'That Username is already taken')
                return redirect('register') #redirect to register with the above message
            else:
                #Check if mail match
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email already exits')
                    return redirect('register')
                else:
                    #if all checks out, then create a user model, with all the recieved attributes
                    user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
                    user.save() #save the user
                    messages.success(request, 'You are registered and can log in')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password) #authenticate and store the detail in a variable

        if user is not None: #if user exist
            auth.login(request, user) #login the user
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login') #else redirect
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logged Out Succesfully')
        return redirect('index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')