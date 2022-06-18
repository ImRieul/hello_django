from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages

from pybo.forms import QuestionForm
from pybo.models import Question


@login_required(login_url='common:login')  # login이 필요한 함수, 로그인 하지 않았으면 login_url로 이동됨
def create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():  # 폼 유효성 검사, 값이 제대로 입력되어 있는지
            question = form.save(commit=False)  # Question 클래스 형식으로 저장(DB에 저장 false)
            question.create_date = timezone.now()  # create_date 저장
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')  # login이 필요한 함수
def modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # question_id로 Question을 찾음, 찾을 수 없을 땐 404
    if request.user != question.author:
        messages.error(request, 'Not Gave Modify')
        return redirect('pybo:detail', question_id=question_id)
    if request.method == "POST":  # 수정한 내용을 전송받을 때
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)  # 기존 내용을 요청받을 때
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, 'Not Gave Delete')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, "Can't recommend to your writing")
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)
