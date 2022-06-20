import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter()
def mark(value):
    # nl12br = 줄바꿈을 <br>로 바꿔줌
    # fenced_code = 마크다운 소스코드
    extansions = ['nl2br', 'fenced_code']
    return mark_safe(markdown.markdown(value, extansions=extansions))