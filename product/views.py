from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.db.models.query import EmptyQuerySet
from django.db.models import Q
from .models import Product, Comment
from .forms import ProductCreateForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from .utils import page_clean_url, sort_clean_url, recreate_url, get_search, get_back_filter_params, get_front_filter_params 


SORT_BY = {'date':'-created_at', 'pricelow':'price', 'pricehigh':'-price'}


def index(request):
    if request.user.is_authenticated and request.user.seller:
            return redirect('user:pending')

    just_arrived   = Product.objects.filter(approved=True).order_by('-created_at')[:8]
    trendy = Product.objects.filter(approved=True).order_by('-created_at')[8:16]
    # high rates - recommended
    context = {'just_arrived':just_arrived, 'trendy':trendy}
    return render(request, 'index.html', context=context)





class CategoryView(ListView):
    model = Product
    template_name = 'shop.html'
    paginate_by = 10


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.seller:
            return redirect('user:pending')
        return super().get(self, request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = self.request.build_absolute_uri()
        ' remove page number'
        clean_url = page_clean_url(url)
        ' recreate url with new filters'
        page_url = recreate_url(clean_url, self.request.GET.get('page_url', ''))
        context['page_url'] = page_url
        context['sort_url'] = sort_clean_url(page_url)

        front = get_front_filter_params(self.request.GET)
        context['price']  = front[0]
        context['colors'] = front[1]
        context['sizes']  = front[2]
        context['gender'] = front[3]

        return context
    

    def get_ordering(self):
        sort_by = self.request.GET.get('sort_by', '')
        return SORT_BY.get(sort_by, self.ordering)
        

    def get_queryset(self):
        object_list = self.model.objects.filter(approved = True)

        sort_by        = self.get_ordering()
        search         = self.request.GET.get('Search', '')
        search_by_name = self.request.GET.get('Search_name', '')
        category       = self.request.GET.get('Category','')

        page_url = self.request.GET.get('page_url', '')
        if page_url:
            params = get_search(page_url)
            search         = params.get('Search', '')
            search_by_name = params.get('Search_name', '')
            category       = params.get('Category','')
            sort_by        = SORT_BY.get(params.get('sort_by',''), self.ordering) 

        if sort_by:
            object_list = object_list.order_by(sort_by)

        if search_by_name:
            object_list = object_list.filter(name__contains = search_by_name)
        elif search:
            object_list = object_list.filter(Q(name__contains = search) | Q(brand = search) | Q(details__contains = search) | Q(description__contains = search))
        elif category:
            object_list = object_list.filter(category=category)


        filters = get_back_filter_params(self.request.GET)
        price  = filters[0]
        color  = filters[1]
        size   = filters[2]
        gender = filters[3]

        if price:
            object_list = object_list.filter(price__range = price)

        if color:
            object_list = object_list.filter(Q(color1__in = color) | 
                                             Q(color2__in = color) |
                                             Q(color3__in = color) |
                                             Q(color4__in = color) |
                                             Q(color5__in = color) 
                                             )

        if size:
            object_list = object_list.filter(Q(size1__in = size) |
                                             Q(size2__in = size) |
                                             Q(size3__in = size) |
                                             Q(size4__in = size) |
                                             Q(size5__in = size) |
                                             Q(size6__in = size)
                                             )

        if gender:
            object_list = object_list.filter(suitable__in = gender)

        return object_list



class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.filter(approved=True)
    template_name = 'detail.html'
    

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.seller:
            return redirect('user:pending')
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(product = self.get_object())
        context['popular'] = Product.objects.order_by('created_at')[:8]
        return context







# def staff(user):
#     return user.is_staff


# @user_passes_test(staff, login_url='/login' )
# def dashboard(request):
#     qs = Product.objects.filter(created_by = request.user)
#     return render(request, 'dashboard.html', {'products': qs})





class DashboardPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):

    login_url = '/login'
    permission_denied_message = 'Only company staff have access to this page'

    def test_func(self):
        return self.request.user.is_staff


class ProductCreateView(DashboardPermissionMixin, CreateView):
    form_class = ProductCreateForm
    template_name = 'dashboard.html'
    success_url = reverse_lazy('product:dashboard')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.created_by = self.request.user 
        product.save()
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(created_by = self.request.user)
        return context



class ProductDeleteView(DashboardPermissionMixin, DeleteView):
    model = Product
    template_name ='error/403.html'
    success_url = reverse_lazy('product:dashboard')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
