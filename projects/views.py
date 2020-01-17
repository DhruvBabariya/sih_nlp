import json
import os
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.conf import settings
from .models import Project
from .forms import ProjectForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .vader import sentiment_score
from .rating_model import rate_review
from .sentimentsAlgo import reviews_preprocessing, sentiment_scores, generate_particular_sentiments
from .word_cloud import generate_word_cloud


@login_required(login_url='/login')
def projects(request):
    querysets = Project.objects.filter(user=request.user)
    context = {
        'querysets': querysets
    }
    return render(request, 'projects/projects.html', context)


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


def data(request, pk, key):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    querysets = Project.objects.filter(pk=pk, user=request.user)
    filename = querysets.values('document')[0]['document']
    file = os.path.join(settings.MEDIA_ROOT, filename)
    reviews_list = reviews_preprocessing(file, key)
    scores = sentiment_scores(reviews_list)
    sentiment_list, num_of_reviews_sentiment = generate_particular_sentiments(
        scores)

    context = {
        'project': project,
        'sentiment_list': sentiment_list,
        'num_of_reviews_sentiment': num_of_reviews_sentiment
    }
    return context


@login_required(login_url='/login')
def projectchart(request, pk):
    querysets = Project.objects.filter(pk=pk, user=request.user)
    key = querysets.values('key')[0]['key']
    context = data(request, pk, key)
    return render(request, 'projects/projectchart.html', context)


@login_required(login_url='/login')
def projectdetail(request, pk):
    querysets = Project.objects.filter(pk=pk, user=request.user)
    key = querysets.values('key')[0]['key']
    context = data(request, pk, key)
    return render(request, 'projects/projectdetail.html', context)


@login_required(login_url='/login')
def single_review(request):
    if request.method == 'POST':
        sentence = request.POST['sentence']
        sentence = ''.join(sentence.split('\n'))
        rating = rate_review(sentence)
        sentiment_dict = sentiment_score(sentence)
        response = {'sentiment': sentiment_dict, 'rating': rating}

        return HttpResponse(json.dumps(response))
    else:
        return render(request, 'projects/single_review.html')
