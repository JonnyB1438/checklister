from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """
    Add css classes to a filter.

    :param field: a field name.
    :param css: list of css class names.
    :return: return a field with given classes.
    """
    return field.as_widget(attrs={"class": css})
