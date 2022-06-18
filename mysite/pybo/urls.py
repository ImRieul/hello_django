from django.urls import path

from .views import base_view, question_view, answer_view


app_name = 'pybo'

urlpatterns = [
    path('', base_view.index, name='index'),
    path('<int:question_id>/', base_view.detail, name='detail'),    # <int:question_id> -> url을 매개

    path('question/create/', question_view.create, name='question_create'),
    path('question/modify/<int:question_id>/', question_view.modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_view.delete, name='question_delete'),
    path('question/vote/<int:question_id>', question_view.vote, name='question_vote'),

    path('answer/create/<int:question_id>/', answer_view.create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_view.modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_view.delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', answer_view.vote, name='answer_vote'),
]
