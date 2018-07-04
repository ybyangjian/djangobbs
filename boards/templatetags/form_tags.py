__author__ = 'yangjian'
__date__ = '2018/7/3 11:01'

from django import template

register = template.Library()

@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__

@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is_invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is_valid'
    return 'form-control {}'.format(css_class)