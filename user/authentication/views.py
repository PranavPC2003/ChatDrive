from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authentication.models import Student
from django.views import View
from django.views.generic import ListView
from .models import Student, Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def home(request):
    return render(request, "authentication/signin.html")

def signup(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('signin')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('signin')

        if len(username) > 15:
            messages.error(request, "Username must be under 12 characters")

        if len(pass1) < 8:
            messages.error(request, "Password must be at least 8 characters")   
        
        if pass1 != pass2:
            messages.error(request, "Password doesnt match")


        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()
        login(request, myuser)

        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return redirect('index')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('index')

@login_required
def index(request):
    pdfs = Student.objects.filter(user=request.user)
    context = {'pdfs': pdfs}
    return render(request, "authentication/index.html", context)

class StudentView(ListView):
    model = Student
    template_name = 'authentication/index.html'
    context_object_name = 'files'
    paginate_by = 4

    def get_queryset(self):
        return Student.objects.order_by('-id')

def myupload(request):
    if request.method == 'POST':
        return upload_file(request)
    else:
        return render(request, "authentication/myupload.html")


@login_required
def upload_file(request):
    if request.method == 'POST':
        name = request.POST['name']
        owner = request.POST['owner']
        pdf = request.FILES['file']

        # Associate the logged-in user with the uploaded file
        student = Student(user=request.user, name=name, owner=owner, pdf=pdf)
        student.save()

        messages.success(request, 'File uploaded successfully.')
        return redirect('index')
    else:
        messages.error(request, 'File was not uploaded successfully.')
        return redirect('myupload')
    
@login_required
def compose_message(request):
    users = User.objects.all()

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message_content = form.cleaned_data['message']
            attached_file = form.cleaned_data['attached_file']

            receiver_username = request.POST.get('receiver') 
            receiver = User.objects.get(username=receiver_username)

            sender = request.user 

            message = Message(sender=sender, receiver=receiver, subject=subject, message=message_content, attached_file=attached_file)
            message.sent = True
            message.save()

            messages.success(request, 'Message sent successfully!')
            return redirect('inbox')
        else:
            messages.error(request, 'There was an error sending the message.')
    else:
        form = MessageForm()

    return render(request, 'authentication/compose_message.html', {'form': form, 'users': users})


@login_required
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user, sent=True).order_by('-timestamp')
    return render(request, 'authentication/inbox.html', {'received_messages': received_messages})


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    return render(request, 'authentication/view_message.html', {'message': message})

@login_required
def view_sent_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user, sent=True)
    return render(request, 'authentication/view_message.html', {'message': message})

@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user, sent=True).order_by('-timestamp')
    return render(request, 'authentication/sent_messages.html', {'sent_messages': sent_messages})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.user == message.sender or request.user == message.receiver:
        message.delete()
        messages.success(request, 'Message deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this message.')

    if request.user == message.sender:
        return redirect('sent_messages')
    else:
        return redirect('inbox')
    
def delete_file(request, pk):
    pdfs = get_object_or_404(Student, pk=pk)
    pdfs.delete()
    return redirect('index')
