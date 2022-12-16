from django.views import generic

from .forms import BooleanQueryForm

# Create your views here.


class BooleanQueryView(generic.FormView):

    template_name = "core/boolean_query.html"
    form_class = BooleanQueryForm

    def get_context_data(self, **kwargs):
        context = super(BooleanQueryView, self).get_context_data(**kwargs)
        
        query = self.request.GET.get("query", None)

        if query:
            results = 

        return context

    def form_valid(self, form):

        return self.render_to_response(self.get_context_data(form=form))
