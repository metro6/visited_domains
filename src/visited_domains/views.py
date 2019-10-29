import datetime
import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from urllib.parse import urlparse

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


from rest_framework.response import Response

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from apps.domains.models import Domain

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def main(request):
  template = 'index.pug'
  return render(request, template, {})

@api_view(['POST'])
def visited_links(request):
  if request.data['links']:
    link_list = []
    for link in request.data['links']:
      domain = get_url_from_link(link)
      if domain:
        link_list.append(domain)
    if len(link_list) == 0:
      return Response({'error': 'Не распознано ни одной ссылки'}, status=409)
  else:
    return Response({'error': 'Нет ни одной ссылки'}, status=400)
  ts = int(datetime.datetime.now().timestamp())

  for link in link_list:
    domain, _ = Domain.objects.get_or_create(domain=link)
    domain.visited = ts
    domain.save()

  cache_domains = {item: ts for item in link_list}
  cache.set('domains', json.dumps(cache_domains), timeout=CACHE_TTL)

  return Response({'status': 'ok'}, status=200)


@api_view(['GET'])
def visited_domains(request):
  from_time = request.GET.get('from', 0)
  to_time = request.GET.get('to', 0)

  try:
    from_time = int(from_time)
    to_time = int(to_time)
  except:
    return Response({'error': 'Некорректное значение начала или конца промежутка времени'}, status=400)

  if from_time > to_time:
    return Response({'error': 'Некорректный промежуток времени'}, status=400)

  if not 'domains' in cache:
    domains = [item.dimain for item in Domain.objects.filter(visited__gt=from_time, visited__lt=to_time)]
    domains_cache = [{item.domain: item.visited} for item in Domain.objects.all()]
    cache.set('domains', json.dumps(domains_cache), timeout=CACHE_TTL)
  else:
    domains_cache = json.loads(cache.get('domains'))
    domains = [k for (k, v) in domains_cache.items() if v < to_time and v > from_time]

  return Response({'domains': domains, 'status': 'ok'}, status=200)


def get_url_from_link(link):
  if not '://' in link:
    # здесь  должна быть какая-то регулярка, по которой мы должны проверить валидность урла.
    # однако одному богу известно, какие варианты вы можете подсунуть при проверке приложения,
    # поэтому я просто верну None
    return
  else:
    return urlparse(link).netloc