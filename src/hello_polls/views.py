from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from hello_polls.models import MyPoll, MyChoice

def index(request):
    poll_list = MyPoll.objects.all().order_by('-pub_date')[:3]
    return render_to_response(
              'hello_polls/index.html',
              {'poll_list': poll_list,
               })
    
def detail(request, poll_id):
    p = get_object_or_404(MyPoll, id=poll_id)
    return render_to_response(
              'hello_polls/detail.html',
              {'poll': p
              },
              context_instance=RequestContext(request))
    
def vote(request, poll_id):
    p = get_object_or_404(MyPoll, pk=poll_id)
    try:
        selected_choice = p.mychoice_set.get(pk=request.POST['choice'])
    except (KeyError, MyChoice.DoesNotExist):
        #display voting form
        return render_to_response('hello_polls/details.html',
                                  {'mypoll':p,
                                   'error_message': "You didn't select a choice.",
                                   },
                                  context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('hello_poll_results', args=(p.id,)))

    
def results(request, poll_id):
    p = get_object_or_404(MyPoll, pk=poll_id)
    return render_to_response('hello_polls/results.html',
                             {'poll':p
                              })
    