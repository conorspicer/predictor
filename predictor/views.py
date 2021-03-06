from django.views.generic import TemplateView
from django.views.generic import ListView
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
        # context['totals'] = sorted(UserTotalResult.objects.all(), key=lambda x: x.total_points_scored, reverse=True)
        # context['conorspicer'] = UserWeekResult.objects.filter(user__username = 'conorspicer').order_by('week')
        # context['torinmehmet'] = UserWeekResult.objects.filter(user__username = 'torinmehmet').order_by('week')
        # context['magnusmartinsen'] = UserWeekResult.objects.filter(user__username = 'magnusmartinsen').order_by('week')
        # context['lewismead'] = UserWeekResult.objects.filter(user__username = 'lewismead').order_by('week')
        return context


class TestPage(TemplateView):
    template_name = 'test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HOFPage(TemplateView):
    template_name = "HOF.html"
