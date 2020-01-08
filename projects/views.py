from django.shortcuts import render,redirect
from .forms import ProjectForm

# Create your views here.

def projects(request):
    return render(request,'projects/projects.html')

def createproject(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProjectForm()
        context = {
            'form' : form,
        }
        return render(request,'projects/createproject.html',context)