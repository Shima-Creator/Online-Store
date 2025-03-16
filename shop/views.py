from django.db.models import Sum, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from django.urls import reverse

from shop.models import Product, Shop, Category, SubCategory, Basket, UserOrder, Comments
from users.models import Seller
from .forms import ShopForm, SellerEditForm, AddProductForm, BasketUpdateForm, CommentsForm
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, SalesmanSerializer, \
    BasketSerializer
from .utils import SalesmanMixin


class ProductListView(ListView):
    """Страница со всеми товарами"""
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 24


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
    model = Shop
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
        context['paid_products'] = UserOrder.objects.filter(user_id = self.request.user.id)
        context['sum'] = Basket.objects.all().filter(user_id=self.request.user.id).aggregate(Sum('quantity'))['quantity__sum']
        user_basket = Basket.objects.all().filter(user_id=self.request.user.id)
        total_price = 0

        for basket_product in user_basket:
            total_price += (basket_product.quantity * basket_product.product.price)
        context['basket_products'] = user_basket
        context['total_price'] = total_price
        context['basket_form'] = BasketUpdateForm()

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
            return Product.objects.filter(shop__shop_name=self.kwargs['shop'])


class ProductView(DetailView):
    """Страница с инф-ей о товаре"""
    model = Product
    template_name = 'product_detail.html'
    pk_url_kwarg = 'product_id'
    form_class = CommentsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_id'] = self.kwargs['product_id']
        context['current_product'] = Product.objects.get(id=self.kwargs['product_id'])
        context['comments'] = Comments.objects.filter(product_id=self.kwargs['product_id'])
        context['comment_form'] = CommentsForm()

        return context

    def post(self, request, *args, **kwargs):
        form = CommentsForm(request.POST)
        product_id = self.kwargs['product_id']

        if form.is_valid():
            comment = Comments(
                comment=form.cleaned_data['comment'],  # Replace 'text' with actual field name in form
                product=get_object_or_404(Product, id=product_id),
                user=request.user
            )

            comment.save()

            return redirect('product_detail', product_id=product_id)

        context = self.get_context_data()
        context['comment_form'] = form

        return render(request, self.template_name, context)

class IndexView(View):
    """Index view"""
    def get(self, request):
        return redirect('product_list/')


class SellerProfile(View):
    """Страница профиля продавца"""
    def get(self, request):
        seller = Seller.objects.filter(user_id=request.user.id).first()
        shops = Shop.objects.filter(seller__user_id=request.user.id) if seller else None
        products = Product.objects.filter(shop=shops.first())

        seller_form = SellerEditForm(instance=seller) if seller else SellerEditForm()

        data = {
            'seller': seller,
            'seller_form': seller_form,
            'shops': shops,
            'products':products,
        }

        return render(request, 'seller_profile.html', data)

    def post(self, request):
        seller = Seller.objects.get(user_id=request.user.id)
        shops = Shop.objects.filter(seller__user_id=request.user.id) if seller else None
        products = Product.objects.filter(shop=shops.first())

        print(request.POST)

        if 'delete_photo' in request.POST:
            seller.profile_pic = None
            seller.save()

            return redirect('seller_profile')

        if 'delete_facebook' in request.POST:
            seller.facebook = None
            seller.save()

            return redirect('seller_profile')

        if 'delete_instagram' in request.POST:
            seller.instagram = None
            seller.save()

            return redirect('seller_profile')

        if 'delete_vk' in request.POST:
            seller.vk = None
            seller.save()

            return redirect('seller_profile')

        if 'delete_telegram' in request.POST:
            seller.telegram = None
            seller.save()

            return redirect('seller_profile')

        if seller:
            seller_form = SellerEditForm(request.POST, request.FILES, instance=seller)
        else:
            seller_form = SellerEditForm(request.POST)

        if seller:
            if seller_form.is_valid():
                # Обновляем существующего Seller
                seller = seller_form.save(commit=False)
                seller.save()

        data = {
            'seller': seller,
            'seller_form': seller_form,
            'shops': shops,
            'products': products,
        }

        return render(request, 'seller_profile.html', data)


class AddShop(View):
    """Добавление магазина"""
    def get(self, request):
        shop_form = ShopForm()
        data = {
            'shop_form':shop_form
        }
        return render(request, 'add_shop.html', data)

    def post(self, request):
        shop_form = ShopForm(request.POST, request.FILES)
        seller = Seller.objects.get(user_id=request.user.id)

        if shop_form.is_valid():
            shop = shop_form.save(commit=False)
            shop.seller = seller
            shop.save()

            return HttpResponseRedirect(reverse('seller_profile'))


class AddProduct(View):
    """Добавление товара продавцом"""
    def get(self, request):
        product_form = AddProductForm()
        
        data = {
            'product_form':product_form
        }

        return render(request, 'add_product.html', data)

    def post(self, request):
        product_form = AddProductForm(request.POST, request.FILES)
        shops = Shop.objects.filter(seller__user_id=request.user.id)
        shops_id = []

        for shop in shops:
            shops_id.append(shop.id)

        if product_form.is_valid() and int(request.POST.get('shop')) in shops_id:
            product_form.save()

            return HttpResponseRedirect(reverse('seller_profile'))


class EditProduct(View):
    """Изменение продукта продавцом"""
    def get(self, request, id=None):
        product = Product.objects.get(id=id)
        product_form = AddProductForm(instance=product)
        print(f"{id=}")
        data = {
            'product_form':product_form,
            'product':product
        }

        return render(request, 'edit_product.html', data)

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        product_form = AddProductForm(request.POST, instance=product)
        shops = Shop.objects.filter(seller__user_id=request.user.id)
        shops_id = []

        for shop in shops:
            shops_id.append(shop.id)

        if product_form.is_valid() and int(request.POST.get('shop')) in shops_id:
            product_form.save()
            return HttpResponseRedirect(reverse('seller_profile'))

        data = {
            'product_form': product_form,
            'product': product
        }

        return render(request, 'edit_product.html', data)


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
            s = Shop.objects.get(pk=pk)
            return Response({'salesmans':SalesmanSerializer(s).data})
        elif not pk:
            s = Shop.objects.all()
            return Response({'salesmans': SalesmanSerializer(s, many=True).data})

    def post(self, request):
        serializer = SalesmanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'salesmans': serializer.data}, status=HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        serializer = SalesmanSerializer(Shop.objects.get(pk=pk), data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        Shop.objects.all().delete(pk=pk)
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


class AboutUs(View):
    """Страница описания магазина"""
    def get(self, request):
        return render(request, 'about_us.html')


class Connect(View):
    """Контакты магазина"""
    def get(self, request):
        return render(request, 'contacts.html')


#Shop Functions
def add_product_to_basket(request, product_id):
    """Добавление товара в корзину"""
    if request.method == 'POST':
        user = request.user.id
        basket_item, created = Basket.objects.get_or_create(user_id=user, product_id=product_id)

        if not created:
            basket_item.quantity += 1
            basket_item.save()

        return redirect(request.META.get('HTTP_REFERER'))

def buy_product(request):
    """Покупка товаров из корзины"""
    user = request.user
    basket_products = Basket.objects.filter(user_id=user)

    if request.method == 'POST':

        for b_product in basket_products:

            if b_product.active == True:

                paid_product = UserOrder.objects.filter(product_id=b_product.product_id).first()

                if paid_product:
                    paid_product.quantity += b_product.quantity
                    b_product.product.stock -= b_product.quantity
                    paid_product.save()

                else:
                    UserOrder.objects.get_or_create(user=user, product_id=b_product.product_id, quantity=b_product.quantity, status=UserOrder.Status.PAID)
                    b_product.product.stock -= b_product.quantity

                b_product.product.save()
                b_product.delete()

        return redirect(request.META.get('HTTP_REFERER'))

def activate_product(request, product_id):
    """Выделение предмета из корзины"""
    basket_item = get_object_or_404(Basket, id=product_id, user=request.user)

    if request.method == 'POST':
        form = BasketUpdateForm(request.POST)
        print(request.POST)
        if form.is_valid():
            active_prod = form.cleaned_data['active']
            basket_item.active = active_prod
            basket_item.save()

            return redirect(request.META.get('HTTP_REFERER'))

def delete_product_from_shop(request, product_id):
    """Удаление товара продавцом"""
    if request.method == 'POST':

        shop_product = Product.objects.all().get(id=product_id)

        shop_product.hard_delete()

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
