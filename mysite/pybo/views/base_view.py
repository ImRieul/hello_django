from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from pybo.models import Question


def index(request):
    page = request.GET.get('page', '1')  # http GET method의 파라미터 page default를 1로 설정 (값이 있으면 그 값을 가져옴)
    keyword = request.GET.get('keyword', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if keyword:
        question_list = question_list.filter(
            Q(subject__icontains=keyword) |
            Q(content__icontains=keyword) |
            Q(answer__content__icontains=keyword) |
            Q(author__username__icontains=keyword) |
            Q(answer__author__username__icontains=keyword)
        ).distinct()
    paginator = Paginator(question_list, 10)  # 게시글 페이지 기준은 10개
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'keyword': keyword}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
