from lib2to3.fixes.fix_input import context

from .models import *

class SalesmanMixin:
    def get_salesman_context(self, **kwargs):
        context = kwargs
        context['shop'] = self.kwargs['shop']
        context['salesman'] = Salesman.objects.all().get(shop=self.kwargs['shop'])

        return context