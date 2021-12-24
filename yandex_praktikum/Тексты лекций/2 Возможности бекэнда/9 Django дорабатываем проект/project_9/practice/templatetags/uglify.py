from django import template


register = template.Library()


@register.filter
def uglify(field):
    s = []
    i = 1
    for x in field:
        if i % 2 == 0:
            s.append(x.upper())
        else:
            s.append(x.lower())
        i = i + 1
    return ''.join(s)
