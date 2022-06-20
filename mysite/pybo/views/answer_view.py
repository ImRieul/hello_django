from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.contrib import messages
from django.utils import timezone

from pybo.forms import AnswerForm
from pybo.models import Question, Answer


@login_required(login_url='common:login')  # login이 필요한 함수
def create(request, question_id):
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
            return redirect(f"{resolve_url('pybo:detail', question_id=question.id)}#answer_{answer.id}")
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, 'Not Gave Modify')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect(f"{resolve_url('pybo:detail', question_id=answer.question.id)}#answer_{answer.id}")
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, 'Not Gave Delete')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, "Can't recommend to your writing")
    else:
        answer.voter.add(request.user)
    return redirect(f"{resolve_url('pybo:detail', question_id=answer.question.id)}#answer_{answer.id}")
