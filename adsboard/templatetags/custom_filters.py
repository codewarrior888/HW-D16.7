from django import template
from adsboard.models import Post, Comment
from django.template.defaultfilters import date

register = template.Library()


@register.filter
def format_time(value, format_string='d.m.Y  H:i'):
    return date(value, format_string)


@register.filter
def format_date(value, format_string='d.m.Y'):
    return date(value, format_string)


censored_words = set([word.lower() for word in ['shit', 'fucking', 'fuck', 'fucking', 'asshole', 'bitch', 'damn', 'shitty', 'чертов', 'хренов', 'хрен', 'черт', 'сука', 'сукин',
                  'дерьмо', 'дерьмовая',
                  ]])


@register.filter
def censor(value):
    words = value.split()
    result = []
    for word in words:
        if word.lower() in censored_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)


@register.filter(takes_context=True)
def replies_amount(context, **kwargs):
    amount = len(Comment.objects.filter(comment_post=Post.objects.get(pk=context.id)))
    return amount
