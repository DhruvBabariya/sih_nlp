from django.shortcuts import render,redirect, HttpResponseRedirect
from .forms import ProjectForm

# Create your views here.

def projects(request):
    return render(request,'projects/projects.html')

def createproject(request):
    if request.method == 'POST':
        user = request.POST['user']

        print(user)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print("FOrm invalid")
            print(form.errors)
        return redirect('index')
    else:
        form = ProjectForm()
        context = {
            'form' : form,
        }
        return render(request,'projects/createproject.html',context)