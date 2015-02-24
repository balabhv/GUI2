from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from polls.forms import CreatePollForm
from django.shortcuts import render_to_response
from registration.views import myAccount
import datetime

from django.core import serializers

from polls.models import Poll, Category, Choice
from polls.models import Question, Category, Choice, Comment, Vote
import json


def home(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/home_page.html')
    context = RequestContext(request, {
        'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(template.render(context))

def polls(request):
    category_list = Category.objects.order_by('-pub_date')
    template = loader.get_template('polls/polls.html')

    politics_list = Poll.objects.select_related().filter(category=1)
    fashion_list = Poll.objects.select_related().filter(category=2)
    science_list = Poll.objects.select_related().filter(category=3)
    technology_list = Poll.objects.select_related().filter(category=4)
    literature_list = Poll.objects.select_related().filter(category=5)

    context = RequestContext(request, {
        'category_list': category_list,
        'politics_list': politics_list,
        'fashion_list': fashion_list,
        'science_list': science_list,
        'technology_list': technology_list,
        'literature_list': literature_list,
    })
    return HttpResponse(template.render(context))

# def category(request, category_id):
#     latest_category_list = Category.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/poll.html')
#     context = RequestContext(request, {
#                              'latest_category_list': latest_category_list,
#                              })
#     return HttpResponse(template.render(context))

def poll(request, category_id, poll_id):
    context = RequestContext(request)
    q = Question.objects.filter(pk=question_id)
    listL = Choice.objects.filter(question = q)
    choicelists = []
    for l in listL:
        listC = Comment.objects.filter(choice = l)
        choicelists.append({'choice': l, 'comments': listC})
    
    context_dict = {'question': q[0], 'choices': choicelists}

    # Render the response and send it back!
    return render_to_response('polls/poll.html', context_dict, context)

def get_poll_chart(request, poll_id):
    q = Poll.objects.get(pk=poll_id)
    clist = Choice.objects.filter(poll = q)
    choices = {'poll': serializers.serialize('json', [ q, ]), 'choices': []}
    for c in clist:
        choices['choices'].append(serializers.serialize('json', [ c, ]))
    return HttpResponse(json.dumps(choices), content_type="application/json")

def vote(request):
    c = Choice.objects.filter(pk=request.POST['cid'])
    c = c[0]
    c.votes = c.votes + 1
    c.save()
    q = Question.objects.filter(pk=request.POST['qid'])
    q = q[0]
    v = Vote(question=q, choice=c, user=request.user, pub_date=datetime.datetime.now())
    v.save()
    return HttpResponseRedirect("/1/"+request.POST['qid']+"/")

def writecomment(request):
    cp = request.POST['mycomment']
    v = Vote.objects.filter(user=request.user)
    c = Comment(comment_text=cp, choice=v.choice, user=request.user, pub_date=datetime.datetime.now())
    c.save()
    return HttpResponseRedirect("/1/"+request.POST['qid']+"/")

def delete_question(request, question_id):
    q = Question.objects.get(pk=question_id)
    q.delete()
    return HttpResponseRedirect("/")

def about(request):
    template = loader.get_template('polls/about.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def freeze_voting(request, poll_id):
    q = Poll.objects.get(pk=poll_id)
    q.frozen = False if q.frozen else True
    q.save()
    return HttpResponseRedirect("/1/"+question_id+"/")

def create_poll(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new poll to the database.
            form.save(request)

            # Now call the index() view.
            # The user will be shown the homepage.
            return myAccount(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CreatePollForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('polls/create_poll.html', {'form': form}, context)

def get_all_categories(request):
    latest_category_list = Category.objects.order_by('category_text')[:5]

    serialized_obj = serializers.serialize('json', [ latest_category_list, ])

    return HttpResponse(serialized_obj, content_type="application/json")

def get_all_polls(request):
    latest_category_list = Category.objects.order_by('category_text')[:5]

    serialized_obj = serializers.serialize('json', [ latest_category_list, ])

    return HttpResponse(serialized_obj, content_type="application/json")
