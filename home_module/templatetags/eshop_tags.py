import markdown
from django.utils.safestring import mark_safe
import bleach
from django import template

register = template.Library()
ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1',
                'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'div']
ALLOWED_ATTRIBUTES = ['href', 'style', 'target']


@register.filter(name='markdown')
def markdown_filter(text):
    clean_text = bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return mark_safe(markdown.markdown(clean_text))
