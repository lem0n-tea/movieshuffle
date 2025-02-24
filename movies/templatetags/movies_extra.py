from django import template
from django.http import QueryDict

register = template.Library()

@register.filter
def exclude_page_param(param_string):
    new = QueryDict(query_string=param_string, mutable=True)
    new.pop('page', None)
    return new.urlencode()