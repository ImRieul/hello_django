from django.contrib import admin

from pybo.models import Question


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


# Register your models here.
admin.site.register(Question, QuestionAdmin)
