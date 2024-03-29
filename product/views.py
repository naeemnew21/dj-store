from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import Q
from .models import Product, Comment, ColorModel, SizeModel, Statics
from .forms import ProductCreateForm
from django.urls import reverse_lazy
from .utils import page_clean_url, sort_clean_url, recreate_url, get_search, get_back_filter_params, get_front_filter_params 
from project.settings import CART_SESSION_ID_KEY
from django.db.models.query import EmptyQuerySet
from cart.models import Order, NonUserOrder
from chartjs.views.lines import BaseLineChartView
        

SORT_BY = {'date':'-created_at', 'pricelow':'price', 'pricehigh':'-price'}


def cart_products(request):
    user = request.user
    user_cart_id = request.COOKIES.get(CART_SESSION_ID_KEY)
    if user.is_authenticated:
        orders = Order.objects.filter(user = user, confirmed = False)
        prods = [i.product for i in orders]
        return prods

    if user_cart_id == None:
        return []
    
    orders = NonUserOrder.objects.filter(user_cart_id = user_cart_id)
    prods = [i.product for i in orders]
    return prods



def index(request):
    if request.user.is_authenticated and request.user.seller:
            return redirect('user:pending')

    just_arrived   = Product.objects.filter(approved=True).order_by('-created_at')[:8]
    trendy = Product.objects.filter(approved=True).order_by('-created_at')[8:16]
    cart_items   = cart_products(request)
    # high rates - recommended
    context = {'just_arrived':just_arrived, 'trendy':trendy, 'cart_items':cart_items}
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

        cart_items   = cart_products(self.request)
        context['cart_items'] = cart_items
        context['statics'], created = Statics.objects.get_or_create(id = 0)

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
            # for i in color:
            object_list = object_list.filter(colors__color__in = color)

        if size:
            # for i in size:
            object_list = object_list.filter(sizes__size__in = size)

        if gender:
            object_list = object_list.filter(suitable__in = gender)

        return list(set(object_list))



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
        context['comments']     = Comment.objects.filter(product = self.get_object())
        context['comments_num'] = len(context['comments'])
        context['popular']      = Product.objects.order_by('created_at')[:8]
        cart_items   = cart_products(self.request)
        context['cart_items'] = cart_items
        
        return context


    def post(self, request, *args, **kwargs):
        if not(request.user.is_authenticated):
            return redirect("user:login")

        rate = request.POST.get('rate', 0)
        comment = request.POST.get('comment','')
        
        user = request.user
        product = self.get_object()

        try:
            review, created = Comment.objects.get_or_create(user=user, product=product)
        except:
            return redirect("product:detail", slug=product.slug)

        review.rate = rate
        review.comment = comment
        review.save()

        return redirect("product:detail", slug=product.slug)







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
        context['colors']   = ColorModel.objects.all()
        context['sizes']   = SizeModel.objects.all()
        selled = 0
        price  = 0
        good = 0
        pending = 0
        for i in context['products']:
            selled += i.selled
            price += i.selled * i.price
            if i.selled > 0:
                good += 1
            if not(i.approved):
                pending += 1
        context['total_selled']   = selled
        context['total_price']   = price
        context['total_good']   = good
        context['total_pending']   = pending
        return context


class ProductDeleteView(DashboardPermissionMixin, DeleteView):
    model = Product
    template_name ='error/403.html'
    success_url = reverse_lazy('product:dashboard')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)



class ProductUpdateView(DashboardPermissionMixin, UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'dashboard.html'
    success_url = reverse_lazy('product:dashboard')


    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(created_by=self.request.user)




class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[35, 44, 25, 11, 44, 16, 35],
                [41, 40, 18, 3, 33, 48, 22],
                [17, 21, 12, 3, 22, 13, 12]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()