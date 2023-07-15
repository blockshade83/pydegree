# https://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code

from django import template
register = template.Library()

@register.simple_tag
def define(val=None):
  return val
