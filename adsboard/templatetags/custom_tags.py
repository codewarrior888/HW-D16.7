from django import template
from django.contrib.auth.models import User
from django.shortcuts import redirect

from adsboard.models import OTPCode

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()


@register.simple_tag(takes_context=True)
def url_address(context, **kwargs):
    return redirect('email_verification', pk=User.objects.get(username=context["user"]).id)


@register.simple_tag(takes_context=True)
def code_gen(context, **kwargs):
    return OTPCode.objects.get(related_user=User.objects.get(username=context["user_display"])).code
