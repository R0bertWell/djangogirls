from django.views.generic import TemplateView
from mysite import urls
class HomePageView(TemplateView):
    template_name = 'home.html'


class ProjetosPageView(TemplateView):
    template_name = 'projetos.html'
