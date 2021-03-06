import json
import os
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.conf import settings
from .models import Project, ProjectResults, ContextResults
from .forms import ProjectForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .vader import sentiment_score
from .rating_model import rate_review
from .sentimentsAlgo import reviews_preprocessing, sentiment_scores, generate_particular_sentiments
from .rating_prediction import predict_rating_dataset, original_rating_dataset
from .aspect_rating import get_aspects_list, give_aspect_rating
from .tweetsAlgos import getTweets


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
    # sentiment_dict, num_of_reviews_sentiment = generate_particular_sentiments(
    #     scores)
    partitioned_sentiment_dict, num_of_reviews_sentiment = generate_particular_sentiments(
        scores, 10)

    context = {
        'project': project,
        # 'sentiment_dict': sentiment_dict,
        'partitionend_sentiments_dict': partitioned_sentiment_dict,
        'num_of_reviews_sentiment': num_of_reviews_sentiment
    }

    return context


@login_required(login_url='/login')
def projectchart(request, pk):
    querysets = Project.objects.filter(pk=pk, user=request.user)
    queryset = querysets[0]
    result = ProjectResults.objects.filter(project=queryset)

    if result:

        num_of_reviews_sentiment = {
            "positive": result[0].positive,
            "negative": result[0].negative,
            "neutral": result[0].neutral
        }
        context = {
            'project': queryset,
            # 'sentiment_dict': sentiment_dict,
            'partitionend_sentiments_dict': result[0].percentages,
            'num_of_reviews_sentiment': num_of_reviews_sentiment
        }

        return render(request, 'projects/projectchart.html', context)
    else:
        key = querysets.values('key')[0]['key']
        context = data(request, pk, key)
        obj = ProjectResults(project=context['project'], positive=context['num_of_reviews_sentiment']['positive'], negative=context['num_of_reviews_sentiment']
                             ['negative'], neutral=context['num_of_reviews_sentiment']['neutral'], percentages=json.dumps(context['partitionend_sentiments_dict']))
        obj.save()
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


@login_required(login_url='/login')
def projectcontext(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    querysets = Project.objects.filter(pk=pk, user=request.user)
    queryset = querysets[0]
    context_result = ContextResults.objects.filter(project=queryset)
    key = querysets.values('key')[0]['key']
    file = querysets.values('document')[0]['document']
    filename = os.path.join(settings.MEDIA_ROOT, file)
    aspects_arr = querysets.values('aspects')[0]['aspects'].split(',')
    aspects_dict = {}
    for aspect in aspects_arr:
        aspects_dict[aspect.strip()] = []

    if context_result:
        original_average_rating = context_result[0].original_average_rating
        predicted_average_rating = context_result[0].predicted_average_rating
        num_of_reviews = context_result[0].num_of_reviews
        accuracy = round((predicted_average_rating / original_average_rating) * 100, 2)
        aspects_rating = json.loads(context_result[0].aspects_rating)
    else:
        original_average_rating, num_of_reviews = original_rating_dataset(filename, 'overall')
        predicted_average_rating = predict_rating_dataset(filename, key)
        accuracy = round((predicted_average_rating / original_average_rating) * 100, 2)
        result = get_aspects_list(filename, key, aspects_dict)
        aspects_rating = give_aspect_rating(result)
        obj = ContextResults(project=queryset,original_average_rating=original_average_rating, predicted_average_rating=predicted_average_rating,num_of_reviews=num_of_reviews, aspects_rating=json.dumps(aspects_rating))
        obj.save()


    context = {
        'project': project,
        'original_average_rating': original_average_rating,
        'predicted_average_rating': predicted_average_rating,
        'accuracy': accuracy,
        'num_of_reviews': num_of_reviews,
        'aspects_rating': aspects_rating
    }

    return render(request, 'projects/projectcontext.html', context)
