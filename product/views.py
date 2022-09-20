from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.query import EmptyQuerySet
from django.db.models import Q
from .models import Product, Comment
from .utils import clean_url, page_clean_url, sort_clean_url




def index(request):
    
    just_arrived   = Product.objects.order_by('created_at')[:8]
    trendy = Product.objects.order_by('created_at')[8:16]
    # high rates - recommended
    context = {'just_arrived':just_arrived, 'trendy':trendy}
    return render(request, 'index.html', context=context)





class CategoryView(ListView):
    model = Product
    template_name = 'shop.html'
    paginate_by = 2


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = self.request.build_absolute_uri()
        context['page_url'] = page_clean_url(url)
        context['sort_url'] = sort_clean_url(url)
        return context
    
    def get_ordering(self):
        sort_by = self.request.GET.get('sort_by', '')
        if sort_by == 'date':
            return '-created_at'
        elif sort_by == 'pricelow':
            return 'price'
        elif sort_by == 'pricehigh':
            return '-price'
        else:
            return self.ordering
        

    def get_queryset(self):
        object_list = self.model.objects.all()

        if self.get_ordering():
            object_list = object_list.order_by(self.get_ordering())
 
        search         = self.request.GET.get('Search', '')
        search_by_name = self.request.GET.get('Search_name', '')
        category       = self.request.GET.get('Category','')

        price  = self.request.GET.get('Price', '')
        color  = self.request.GET.get('Color', '')
        size   = self.request.GET.get('Size', '')
        gender = self.request.GET.get('Gender', '')

        if search_by_name:
            object_list = object_list.filter(name__contains = search_by_name)
        elif search:
            object_list = object_list.filter(Q(name__contains = search) | Q(brand = search) | Q(details__contains = search) | Q(description__contains = search))

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
    return render(request, 'dashboard.html')