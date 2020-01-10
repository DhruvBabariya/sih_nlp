from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .vader import sentiment_scores
import json

# Create your views here.
@login_required(login_url='/login')
def projects(request):
    querysets = Project.objects.filter(user=request.user)
    context = {
        'querysets': querysets
    }
    return render(request, 'projects/projects.html', context)


@login_required(login_url='/login')
def projectchart(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    context = {
        'project': project
    }
    return render(request, 'projects/projectchart.html', context)


@login_required(login_url='/login')
def projectdetail(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    context = {
        'project': project
    }
    return render(request, 'projects/projectdetail.html', context)


@login_required(login_url='/login')
def createproject(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            document_form = form.save(commit=False)
            document_form.user = request.user
            document_form.save()
        else:
            print("Invalid form")
        message = "Success"
        return HttpResponse(message)
    else:
        form = ProjectForm()
        context = {
            'form': form,
        }
        return render(request, 'projects/createproject.html', context)


@login_required(login_url='/login')
def single_review(request):
    if request.method == 'POST':
        sentence = request.POST['sentence']
        sentiment_dict = sentiment_scores(sentence)
        return HttpResponse(json.dumps(sentiment_dict))
    return render(request, 'projects/single_review.html')
