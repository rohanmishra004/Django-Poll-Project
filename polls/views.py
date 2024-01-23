from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice,Question
# Create your views here.

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

#USING GENERICS
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"


    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {"question":question})
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request, 
            'polls/detail.html',
            {
                "question":question,
                "error_message":"You didnt select a choice"
            },
        )
    else:
        selected_choice+=1
        selected_choice.save()
        # We are using the reverse() function in the HttpResponseRedirect constructor in this example. This function helps avoid having to hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view
        return HttpResponseRedirect(reverse("polls:results", args=(question_id)))