from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.query import EmptyQuerySet
from .models import Product, Comment





def index(request):
    
    mobile   = Product.objects.filter(category = 'mobile')
    computer = Product.objects.filter(category = 'computer')
    electric = Product.objects.filter(category = 'electric equipment')
    # high rates - recommended
    context = {'mobile':mobile, 'computer':computer, 'electric':electric}
    return render(request, 'index.html', context=context)





class CategoryView(ListView):
    model = Product
    template_name = '/your/template.html'
    
    def get_queryset(self):
        # name = self.kwargs.get('name', '')
        # #query = self.request.GET.get('q')
        # object_list = self.model.objects.all()
        # if name:
        #     object_list = object_list.filter(name__icontains=name)
        # return object_list
        return EmptyQuerySet
    




class ProductDetailView(DetailView):
    model = Product
    pk    = 'slug'
    template_name = '/your/template.html'
    
    # override get_context to get comments and rate