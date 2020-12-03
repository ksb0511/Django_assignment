from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from .models import Choice, Question

# 각 뷰는 두가지 중 하나를 한다. : 1. 요청된 페이지의 내용이 담긴 HttpResponse 객체 반환 2. Http404 같은 예외 발생
# generic뷰 사용 : 코드를 중복적으로 쓰는 경우, 사용
# generic뷰 사용법 : 1. URLconf 변환 2. 불필요한 코드 일부 삭제 3. 장고의 제너릭뷰 기반의 새로운 뷰 도
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# vote() 함수
def vote(request, question_id):
    # get_object_or_404() 함수는 Django 모델을 첫번째 인자로 받고, 몇개의 키워드 인수를 모델 관리자의 get() 함수에 넘긴다.
    # 만약 객체가 존재하지 않을 경우, Http404 예외 발생
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST 는 키로 전송된 자료에 접근할 수 있도록 해주는 사전과 같은 객체
        # request.POST['choice'] 는 선택된 choice의 ID를 문자열로 반환합니다. request.POST 의 값은 항상 문자열들이다.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        # POST 자료에 choice가 없을 경우, request.POST['choice'] 는 KeyError 가 일어남.
        # KeyError 를 체크하고, choice가 주어지지 않은 경우에는 error_message와 함께 설문조사 폼(detail.html)을 다시 보여줌.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# choice 수가 증가한 이후에는 HttpResponse 가 아닌 HttpResponseRedirect 를 반환
# HttpResponseRedirect 는 하나의 인수를 받는데, 그 인수는 사용자에게 재전송될 url
# HttpResponseRedirect 생성자 안에서 사용되고 있는 함수인 reverse()는 뷰 함수에서 url을 하드코딩하지 않도록 도와준다.
# url패턴의 변수부분을 조합하여, 제어 전달을 하고자 하는 해당 뷰를 가리킨다. -> 'polls:results'
# reverse() 호출은 '/polls/1/results/' 같은 문자열을 반환할 것이고, 가운데에 있는 숫자 1은 question.id 값을 의미한다.
# 이렇게 리디렉션된 url은 최종 페이지를 표시하기 위해 'results' 뷰를 호출한다.

