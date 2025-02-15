
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect

from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from shop.models import Product,  Salesman, Category, SubCategory, Basket
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, SalesmanSerializer, \
    BasketSerializer
from .utils import SalesmanMixin


class ProductListView(ListView):
    """Страница со всеми товарами"""
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


class CategoriesListView(ListView):
    """Страница со списком категорий/подкатегорий"""
    model = Category
    template_name = 'categories_list.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = SubCategory.objects.all()

        return context


class SalesmanListView(ListView):
    """Страница со списком продавцов"""
    model = Salesman
    template_name = 'salesman_list.html'
    context_object_name = 'salesmans'


class ProductsByCategoriesView(ListView):
    """Страница со списком товаров по категории/подкатегории"""
    model = Product
    template_name = 'products_by_categories.html'
    context_object_name = 'filter_product'

    def get_queryset(self):
        if self.kwargs['category'] is not None:
            for product in Product.objects.all():

                if self.kwargs['category'] == product.subcategory.category.name:
                    return Product.objects.filter(subcategory__category=product.subcategory.category.id)

                if self.kwargs['category'] == product.subcategory.name:
                    return Product.objects.filter(subcategory_id=product.subcategory.id)


class BasketView(ListView):
    """Корзина пользователя"""
    model = Basket
    template_name = 'basket.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum'] = Basket.objects.all().filter(username_id=self.request.user.id).aggregate(Sum('quantity'))['quantity__sum']
        user_basket = Basket.objects.all().filter(username_id=self.request.user.id)
        total_price = 0

        for basket_product in user_basket:
            total_price += (basket_product.quantity * basket_product.product.price)
        context['basket_products'] = user_basket
        context['total_price'] = total_price

        return context


class SalesmanView(SalesmanMixin, ListView):
    """Страница с инф-ей о продавце"""
    model = Product
    template_name = 'salesman.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        salesman_context = self.get_salesman_context()
        context = dict(list(context.items()) + list(salesman_context.items()))

        return context

    def get_queryset(self):
        if self.kwargs['shop'] is not None:
            return Product.objects.filter(shop__shop=self.kwargs['shop'])


class ProductView(DetailView):
    """Страница с инф-ей о товаре"""
    model = Product
    template_name = 'product_detail.html'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_id'] = self.kwargs['product_id']
        context['current_product'] = Product.objects.all().get(id=self.kwargs['product_id'])

        return context


class IndexView(View):
    """Index view"""
    def get(self, request):
        return redirect('product_list/')


#Serializers
class CategoryAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            c = Category.objects.get(pk=pk)
            return Response({'categories':CategorySerializer(c).data})
        elif not pk:
            c = Category.objects.all()
            return Response({'categories':CategorySerializer(c, many=True).data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'categories':serializer.data}, status=HTTP_201_CREATED)

    def put(self, request, **kwargs):
        pk = kwargs.get('pk')
        serializer = CategorySerializer(Category.objects.get(pk=pk), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        Category.objects.all().delete(pk=pk)
        return Response(status=status.HTTP_200_OK)


class SubCategoryAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            s = SubCategory.objects.get(pk=pk)
            return Response({'subcategories': SubCategorySerializer(s).data})
        elif not pk:
            s = SubCategory.objects.all()
            return Response({'subcategories':SubCategorySerializer(s, many=True).data})

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'subcategories': serializer.data}, status=HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        serializer = SubCategorySerializer(SubCategory.objects.get(pk=pk), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        SubCategory.objects.all().delete(pk=pk)
        return Response(status=status.HTTP_200_OK)


class ProductAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')

        if pk:
            p = Product.objects.get(pk=pk)
            return Response({'products':ProductSerializer(p).data})
        elif not pk:
            p = Product.objects.all()
            return Response({'products': ProductSerializer(p, many=True).data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'products': serializer.data}, status=HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        serializer = ProductSerializer(Product.objects.get(pk=pk), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        Product.objects.all().delete(pk=pk)
        return Response(status=status.HTTP_200_OK)


class SalesmanAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            s = Salesman.objects.get(pk=pk)
            return Response({'salesmans':SalesmanSerializer(s).data})
        elif not pk:
            s = Salesman.objects.all()
            return Response({'salesmans': SalesmanSerializer(s, many=True).data})

    def post(self, request):
        serializer = SalesmanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'salesmans': serializer.data}, status=HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        serializer = SalesmanSerializer(Salesman.objects.get(pk=pk), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        Salesman.objects.all().delete(pk=pk)
        return Response(status=status.HTTP_200_OK)


class BasketAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')

        if pk:
            b = Basket.objects.get(pk=pk)
            return Response({'baskets':BasketSerializer(b).data})

        elif not pk:
            b = Basket.objects.all()
            return Response({'baskets': BasketSerializer(b, many=True).data})

    def post(self, request):
        serializer = BasketSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'baskets': serializer.data}, status=HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        serializer = BasketSerializer(Basket.objects.get(pk=pk), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        Basket.objects.all().delete(pk=pk)
        return Response(status=status.HTTP_200_OK)


#Shop Functions
def add_product_to_basket(request, product_id):
    """Добавление товара в корзину"""
    if request.method == 'POST':
        user = request.user.id
        basket_item, created = Basket.objects.get_or_create(username_id=user, product_id=product_id)

        if not created:
            basket_item.quantity += 1
            basket_item.save()

        return redirect(request.META.get('HTTP_REFERER'))

def delete_product_from_basket(request, product_id):
    """Уменьшение количества товара в корзине"""
    if request.method == 'POST':

        basket_product = Basket.objects.all().get(id=product_id)

        if basket_product.quantity > 1:
            basket_product.quantity -= 1
            basket_product.save()

        elif basket_product.quantity == 1:
            basket_product.delete()

        return redirect(request.META.get('HTTP_REFERER'))

def add_quantity_basket_product(request):
    """Увеличение количества товара в корзине"""
    if request.method == 'POST':
        change = int(request.POST.get('change'))
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Basket, id=product_id)
        new_quantity = max(0, product.quantity + change)
        product.quantity = new_quantity
        product.save()

        return redirect(request.META.get('HTTP_REFERER'))

def search_product(request):
    """Поиск товара по названию"""
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query))

        return render(request, 'product_list.html', {'products': products})

    return render(request, 'product_list.html')
