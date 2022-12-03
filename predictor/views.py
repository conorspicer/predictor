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
        return context


class TestPage(TemplateView):
    template_name = 'test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HOFPage(TemplateView):
    template_name = "HOF.html"
