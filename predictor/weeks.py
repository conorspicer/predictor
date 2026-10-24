from django.http import Http404
from scripts.get_week import get_week


def selected_week(request, default_current=True):
    value = request.GET.get('week')
    if not value:
        return get_week() if default_current else 'All'
    if value == 'All':
        return value
    try:
        week = int(value)
    except (TypeError, ValueError):
        raise Http404('Select a valid week.')
    if not 1 <= week <= 23:
        raise Http404('Select a valid week.')
    return week
