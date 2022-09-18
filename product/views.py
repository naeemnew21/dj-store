from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.query import EmptyQuerySet
from .models import Product, Comment
from .filter import ProductFilter





def index(request):
    
    just_arrived   = Product.objects.order_by('created_at')[:8]
    trendy = Product.objects.order_by('created_at')[8:16]
    # high rates - recommended
    context = {'just_arrived':just_arrived, 'trendy':trendy}
    return render(request, 'index.html', context=context)





class CategoryView(ListView):
    model = Product
    template_name = 'shop.html'
    
    def get_queryset(self):
        object_list = self.model.objects.all()
 
        search = self.request.GET.get('Search', '')
        category = self.request.GET.get('Category','')

        price = self.request.GET.get('Price', '')
        color = self.request.GET.get('Color', '')
        size = self.request.GET.get('Size', '')
        gender = self.request.GET.get('Gender', '')

        if search:
            myfilter = ProductFilter(self.request.GET, queryset=object_list)
            object_list = myfilter.qs

        elif category:
            object_list = object_list.filter(category=category)


        if price:
            start = 0
            end = 1000
            #object_list = object_list.filter(price__range=(start, end))

        if color:
            colors = []
            #object_list = object_list.filter(color__in=colors)

        if size:
            sizes = []
            #object_list = object_list.filter(size__in=sizes)

        if gender:
            gender_list = []
            #object_list = object_list.filter(suitable__in=gender_list)

        return object_list



class ProductDetailView(DetailView):
    model = Product
    pk = 'slug'
    template_name = 'detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(product = self.get_object())
        context['popular'] = Product.objects.order_by('created_at')[:8]
        return context



def dashboard(request):
    return render(request, 'dashboard.html',)