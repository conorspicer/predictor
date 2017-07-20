from django.views.generic import TemplateView
from django.views.generic import ListView
from results.models import UserWeekResult, UserTotalResult
from django.contrib.auth import get_user_model
User = get_user_model()

class HomePage(ListView):
    context_object_name = 'results_on_home'
    template_name = 'index.html'

    def get_queryset(self):
        qs = User.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['totals'] = UserTotalResult.objects.all().order_by('-total_points_scored')
        context['conorspicer'] = UserWeekResult.objects.filter(user__username = 'conorspicer').order_by('week')
        context['torinmehmet'] = UserWeekResult.objects.filter(user__username = 'torinmehmet').order_by('week')
        context['magnusmartinsen'] = UserWeekResult.objects.filter(user__username = 'magnusmartinsen').order_by('week')
        context['lewismead'] = UserWeekResult.objects.filter(user__username = 'lewismead').order_by('week')
        return context

class TestPage(TemplateView):
    template_name = 'test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'

#
# class HomePage(TemplateView):
#     template_name = "index.html"

class HOFPage(TemplateView):
    template_name = "HOF.html"
