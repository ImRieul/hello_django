from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question


# Create your views here.


def index(request):
    page = request.GET.get('page', '1')         # http GET method의 파라미터 page default를 1로 설정 (값이 있으면 그 값을 가져옴)
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)    # 게시글 페이지 기준은 10개
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


# 하나의 view로 신규 질문 페이지(get, a태그로 접속시)과, 질문 저장(post)을 같이 처리하고 있다.
@login_required(login_url='common:login')   # login이 필요한 함수, 로그인 하지 않았으면 login_url로 이동됨
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():     # 폼 유효성 검사
            question = form.save(commit=False)      # Question 클래스 형식으로 저장(DB에 저장 false)
            question.create_date = timezone.now()   # create_date 저장
            question.author = request.user          # author 속성에 로그인 계정 저장
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')   # login이 필요한 함수
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # return redirect('pybo:detail', question_id=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)