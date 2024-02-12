from home.serializers import *
from home.utils import send_code
from rest_framework import status
from django.db import transaction
from django.urls import reverse_lazy
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from home.forms import StudentSignUpForm, CodeForm, UserUpdateForm
from django.core.paginator import (Paginator, PageNotAnInteger, EmptyPage)
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

def main(request):
    info = Information.objects.all()
    category = Category.objects.filter(status='Yes').order_by('-id')
    product = Product.objects.filter(status='Yes').order_by('?')[:12]
    product_all = Product.objects.filter(status='Yes').order_by('-id')
    context = {
        'info':info,
        'category':category,
        'product':product,
        'product_all':product_all,
    }
    return render(request, 'main.html', context)

def product_detail(request, code):
    product = Product.objects.get(code=code)
    elements = Product_Elements.objects.filter(product__code=code, status='Yes')
    comments = Comment.objects.filter(product__code=code, status='Yes').order_by('-id')[:2]
    products_all = Product.objects.filter(status='Yes').order_by('?')[:8]
    product_slider = Product.objects.filter(status='Yes').order_by('?')[:9]
    category = Category.objects.filter(status='Yes').order_by('-id')
    info = Information.objects.all().order_by('-id')[:1]
    client = None
    if request.user.is_authenticated:
        client = Client.objects.get(user=request.user)
    else:
        pass
    new_price = product.new_price
    old_price = product.old_price
    if old_price > 0 and new_price < old_price:
        discount_percentage = ((old_price - new_price) / old_price) * 100
    else:
        discount_percentage = 0
    comment_all = Comment.objects.filter(product__code=code, status='Yes')
    total_comments = comment_all.count()
    comment_5 = comment_all.filter(rate=5)
    only_5 = (comment_5.count() / total_comments) * 100 if total_comments > 0 else 0
    comment_4 = comment_all.filter(rate=4)
    only_4 = (comment_4.count() / total_comments) * 100 if total_comments > 0 else 0
    comment_3 = comment_all.filter(rate=3)
    only_3 = (comment_3.count() / total_comments) * 100 if total_comments > 0 else 0
    comment_2 = comment_all.filter(rate=2)
    only_2 = (comment_2.count() / total_comments) * 100 if total_comments > 0 else 0
    comment_1 = comment_all.filter(rate=1)
    only_1 = (comment_1.count() / total_comments) * 100 if total_comments > 0 else 0
    total_count_product = product.total_count
    order_count = product.order_count
    total_amount = total_count_product - order_count if total_count_product > 0 else 0
    context = {
        'product':product,
        'products_all':products_all,
        'elements':elements,
        'comments':comments,
        'product_slider':product_slider,
        'category':category,
        'client':client,
        'info':info,
        'discount_percentage':discount_percentage,
        'only_5':only_5,
        'only_4':only_4,
        'only_3':only_3,
        'only_2':only_2,
        'only_1':only_1,
        'total_amount':total_amount,
    }
    return render(request, 'pages/product-detail.html', context)

def filter_products(request, code):
    category = Category.objects.filter(status='Yes')
    category_all = Category.objects.get(code=code)
    info = Information.objects.all().order_by('-id')[:1]
    product_filter = Product.objects.filter(category__code=code, status='Yes')
    paginator = Paginator(product_filter, 8)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        product_filter = paginator.page(page)
    except PageNotAnInteger:
        product_filter = paginator.page(1)
    except EmptyPage:
        product_filter = paginator.page(paginator.num_pages)
    context = {
        'info':info,
        'category':category,
        'category_all':category_all,
        'product_filter':product_filter,
    }
    return render(request, 'pages/filter_product.html', context)

@login_required(login_url='login_form')
def shopcart(request):
    info = Information.objects.all().order_by('-id')[:1]
    client = Client.objects.get(user=request.user)
    shopcart = Shopcart.objects.filter(client=client)
    category = Category.objects.filter(status='Yes')
    total = 0
    for rs in shopcart:
        total += rs.product.new_price * rs.quantity
    context = {
        'client':client,
        'shopcart':shopcart,
        'total':total,
        'category':category,
        'info':info,
    }
    return render(request, 'order/ShopCart.html', context)

@login_required(login_url='login_form')
def delete_cart(request, id):
    shopcart = Shopcart.objects.get(pk=id)
    shopcart.delete()
    return redirect('shopcart')

@login_required(login_url='login_form')
def order(request):
    client = Client.objects.get(user=request.user)
    shopcart = Shopcart.objects.filter(client=client)
    category = Category.objects.filter(status='Yes')
    info = Information.objects.all().order_by('-id')[:1]
    total = 0
    total_qty = 0
    for rs in shopcart:
        total_qty += rs.quantity
        total += rs.product.new_price * rs.quantity
    context = {
        'client':client,
        'shopcart':shopcart,
        'category':category,
        'total':total,
        'total_qty':total_qty,
        'info':info,
    }
    return render(request, 'order/order.html', context)

def contact(request):
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    context = {
        'info':info,
        'category':category
    }
    return render(request, 'pages/contact.html', context)

def aboutus(request):
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    context = {
        'info':info,
        'category':category,
    }
    return render(request, 'pages/aboutus.html', context)

def newshop(request):
    news = News.objects.filter(status='Yes').order_by('-id')
    product = Product.objects.filter(status='Yes').order_by('?')[:7]
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    paginator = Paginator(news, 1)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    context = {
        'news':news,
        'info':info,
        'category':category,
        'product':product,
    }
    return render(request, 'pages/newshop.html', context)

def news_detail(request, code):
    news = News.objects.get(code=code)
    news_comment = News_comment.objects.filter(news__code=code).order_by('-id')[:2]
    category = Category.objects.filter(status='Yes')
    info = Information.objects.all().order_by('-id')[:1]
    news_comment_all = News_comment.objects.filter(news__code=code, status='Yes')
    total_comments = news_comment_all.count()
    comment_news_5 = news_comment_all.filter(rate=5)
    only_news_5 = (comment_news_5.count() / total_comments) * 100 if total_comments > 0 else 0
    comment_news_4 = news_comment_all.filter(rate=4)
    only_news_4 = (comment_news_4.count() / total_comments) * 100 if total_comments > 0 else 0
    comment_news_3 = news_comment_all.filter(rate=3)
    only_news_3 = (comment_news_3.count() / total_comments) * 100 if total_comments > 0 else 0
    comment_news_2 = news_comment_all.filter(rate=2)
    only_news_2 = (comment_news_2.count() / total_comments) * 100 if total_comments > 0 else 0
    comment_news_1 = news_comment_all.filter(rate=1)
    only_news_1 = (comment_news_1.count() / total_comments) * 100 if total_comments > 0 else 0
    context = {
        'news':news,
        'news_comment':news_comment,
        'category':category,
        'info':info,
        'only_news_5': only_news_5,
        'only_news_4': only_news_4,
        'only_news_3': only_news_3,
        'only_news_2': only_news_2,
        'only_news_1': only_news_1,
    }
    return render(request, 'pages/news_detail.html', context)

def faq(request):
    faq = Faq.objects.filter(status='Yes')
    category = Category.objects.filter(status='Yes')
    info = Information.objects.all().order_by('-id')[:1]
    context = {
        'faq':faq,
        'category':category,
        'info':info,
    }
    return render(request, 'pages/faq.html', context)


@login_required(login_url='login_form')
def client(request):
    client = Client.objects.get(user=request.user)
    order_client = Order.objects.filter(client=client).order_by('-id')
    category = Category.objects.filter(status='Yes')
    info = Information.objects.all().order_by('-id')[:1]
    paginator = Paginator(order_client, 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        order_client = paginator.page(page)
    except PageNotAnInteger:
        order_client = paginator.page(1)
    except EmptyPage:
        order_client = paginator.page(paginator.num_pages)
    context = {
        'category':category,
        'info':info,
        'client':client,
        'order_client':order_client,
    }
    return render(request, 'account/client.html', context)

@login_required(login_url='login_form')
def order_detail(request, code):
    client = Client.objects.get(user=request.user)
    order_client = Order.objects.get(code=code)
    category = Category.objects.filter(status='Yes')
    info = Information.objects.all().order_by('-id')[:1]
    context = {
        'client':client,
        'order_client':order_client,
        'category':category,
        'info':info,
    }
    return render(request, 'order/order_detail.html', context)


@login_required(login_url='login_form')
def payment(request):
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    client = Client.objects.get(user=request.user)
    context = {
        'info':info,
        'category':category,
        'client':client
    }
    return render(request, 'order/payment.html', context)


def search(request):
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    product = Product.objects.all()[:1]
    context = {
        'info':info,
        'category':category,
        'product':product,
    }
    return render(request, 'pages/search.html', context)
########################################################################################################################
class register(CreateView):
    template_name = 'Authenticate/register_client.html'
    form_class = StudentSignUpForm
    success_url = reverse_lazy('loading_page')
    success_message = "Вы успешно зарегистрировались"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        info = Information.objects.all()[:1]
        kwargs['info'] = info
        category = Category.objects.all()[:1]
        kwargs['category'] = category
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_client:
            request.session['pk'] = user.pk
            return redirect('verify_code')
        else:
            return redirect('login_form')
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    context = {
        'info':info,
        'category':category,
    }
    return render(request, 'Authenticate/login.html', context)

def loading_page(request):
    return render(request, 'Authenticate/loading_page.html')

def verify_code(request):
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.code}"
        if not request.POST:
           print(code_user)
           send_code(code_user, user.email)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request,user)
                return redirect('client')
            else:
               return redirect('verify_code')
    return render(request, 'Authenticate/verify.html', {'form':form, 'info':info, 'category':category,})

@login_required(login_url='login_form')
def update(request):
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    client = Client.objects.get(user=request.user)
    if request.method == 'POST':
        user_manager = UserUpdateForm(request.POST, instance=request.user)
        if user_manager.is_valid():
            user_manager.save()
            return redirect('client')
        else:
            return redirect("update")
    else:
        user_manager = UserUpdateForm(instance=request.user)
        context = {
            'info':info,
            'client':client,
            'user_manager': user_manager,
            'category':category,
        }
        return render(request, 'account/client_update.html', context)

@login_required(login_url='login_form')
def password(request):
    info = Information.objects.all().order_by('-id')[:1]
    category = Category.objects.filter(status='Yes')
    client = Client.objects.get(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('main')
        else:
            return redirect('password')
    else:
        form = PasswordChangeForm(request.user)
        context = {
            'info':info,
            'client':client,
            'category':category,
            'form': form,
        }
        return render(request, 'account/change_password.html', context)

@login_required(login_url='login_form')
def logout_client(request):
    logout(request)
    return redirect('main')
########################################################################################################################
class ShopCart(APIView):
    def post(self, request):
        serilaizer = ShopCartSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderProduct(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        client = Client.objects.get(user=request.user)
        shopcart = Shopcart.objects.filter(client=client)
        order_data = []
        for item in shopcart:
            product = item.product
            total_quantity = sum(item.quantity for item in shopcart)
            total_price = sum(item.calculate_total_price() for item in shopcart)
            if client.user.total_price is None or client.user.total_price == 0 or total_price > client.user.total_price:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            elif item.product.total_count is None or item.product.total_count == 0 or total_quantity > item.product.total_count:
                return Response(status=status.HTTP_404_NOT_FOUND)
            elif client.user.total_price >= total_price and item.product.total_count >= total_quantity:
                client.user.total_price -= total_price
                client.user.save()
                product.total_count -= total_quantity
                product.order_count += total_quantity
                product.save()
                for save in shopcart:
                    order_data.append({
                        'client': client.id,
                        'product': save.product.id,
                        'color': save.color,
                        'quantity': save.quantity,
                        'total_price': save.calculate_total_price(),
                        'first_name': request.data['first_name'],
                        'last_name': request.data['last_name'],
                        'phone': request.data['phone'],
                        'country': request.data['country'],
                        'city': request.data['city'],
                        'address': request.data['address'],
                        'zip_code': request.data['zip_code'],
                        'order_note': request.data['order_note'],
                    })
                serializer = OrderSerializer(data=order_data, many=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    shopcart.delete()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class Comment_to_Product(APIView):
    def post(self, request):
        serilaizer = CommentSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

class Comment_to_News(APIView):
    def post(self, request):
        serilaizer = NewsCommentSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactUs(APIView):
    def post(self, request):
        serilaizer = ContactUsSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTotalPriceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        client = Client.objects.get(user=request.user)
        price = request.data.get('price')
        try:
            price_int = int(price)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if price is not None or price != '':
            client.user.total_price += price_int
            client.user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PaymentPrice(APIView):
    def get(self, request, id):
        payment = User.objects.get(pk=id)
        serializer = PriceSerializer(payment, many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
########################################################################################################################
def search_product(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        res = None
        title = request.POST.get('title')
        qs = Product.objects.filter(title__icontains=title, status='Yes')
        if len(qs) > 0 and len(title) > 0:
            data = []
            for pos in qs:
                avg_rating = pos.count_rate()
                comment_count = pos.count_product()
                item = {
                    'id':pos.id,
                    'title':pos.title,
                    'new_price':pos.new_price,
                    'old_price':pos.old_price,
                    'image': str(pos.image.url),
                    'status':pos.status,
                    'code':pos.code,
                    'count_rate': avg_rating,
                    'count_product': comment_count,
                    'order_count':pos.order_count,
                    'create_at':pos.create_at,
                }
                data.append(item)
            res = data
        else:
            res = "Нет такой информации"
        return JsonResponse({'data':res})
    return JsonResponse({})
########################################################################################################################
def outside_404_not_found(request,exception):
    return render(request, 'error/outside.html',)

def request_500(request):
    return render(request, 'error/500_request.html',)

def request_502_error(request):
    return render(request, 'error/502_home_request.html',)










