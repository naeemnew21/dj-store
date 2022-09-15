from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.query import EmptyQuerySet
from .models import Product, Comment





def index(request):
    
    just_arrived   = Product.objects.order_by('created_at')[:10]
    trendy = Product.objects.order_by('created_at')[10:20]
    # high rates - recommended
    context = {'just_arrived':just_arrived, 'trendy':trendy}
    return render(request, 'index.html', context=context)





class CategoryView(ListView):
    model = Product
    template_name = '/your/template.html'
    
    def get_queryset(self):
        category = self.kwargs.get('Category', '')
        object_list = self.model.objects.all()
        if category:
            object_list = object_list.filter(category=category)
        return object_list
    




class ProductDetailView(DetailView):
    model = Product
    pk    = 'slug'
    template_name = '/your/template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(product = self.get_object())
        return context