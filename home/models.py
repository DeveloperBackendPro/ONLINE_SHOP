import sys
import random
import qrcode
from PIL import Image
from io import BytesIO
from django.db import models
from django.core.files import File
from django.db.models import Avg, Count
from colorfield.fields import ColorField
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files.uploadedfile import InMemoryUploadedFile


class Information(models.Model):
    STATUS = (
        ('Open', 'Открыть'),
        ('Close', 'Закрыто'),
        ('No', 'Нет'),
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    city = models.CharField(max_length=255, verbose_name='Город')
    country = models.CharField(max_length=255, verbose_name='Страна')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    email = models.CharField(max_length=255, verbose_name='Почта')
    about_us = RichTextUploadingField(verbose_name='О нас')
    facebook = models.URLField(max_length=1000, blank=True, null=True, verbose_name='Фейсбук')
    instagram = models.URLField(max_length=1000, blank=True, null=True, verbose_name='Инстаграм')
    youtube = models.URLField(verbose_name='Юутубе', blank=True, null=True,)
    telegram = models.URLField(max_length=1000, blank=True, null=True, verbose_name='Телеграм')
    location = models.URLField(max_length=1000, verbose_name='Геолокация')
    repair = models.TimeField(verbose_name='Время', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS, default='Open', verbose_name='Статусы')
    create_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информация'

class Category(models.Model):
    STATUS = (
        ('Yes', 'Да'),
        ('No', 'Нет'),
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    status = models.CharField(max_length=15, choices=STATUS, default='Yes', verbose_name='Статусы')
    code = models.CharField(max_length=1000, blank=True, null=True, unique=True, verbose_name='Код')
    create_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        code = self.code
        if not code:
            code = get_random_string(8).upper()
        while Category.objects.filter(code=code).exclude(pk=self.pk).exists():
            code = get_random_string(8).upper()
        self.code = code
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def count(self):
        product_count = Product.objects.filter(category=self).aggregate(count=Count('id'))
        cnt = 0
        if product_count["count"] is not None:
            cnt = int(product_count["count"])
        return cnt


class Product(models.Model):
    STATUS = (
        ('Yes', 'Да'),
        ('No', 'Нет'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='product')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description_full = RichTextUploadingField(verbose_name='Описание полное')
    old_price = models.IntegerField(verbose_name='Старая цена')
    new_price = models.IntegerField(verbose_name='Новая цена')
    total_count = models.IntegerField(default=0, verbose_name='Количество продукт')
    order_count = models.IntegerField(default=0,verbose_name='Количество заказов')
    image = models.ImageField(upload_to='images/Product',
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', ])], verbose_name='Изображение')
    status = models.CharField(max_length=15, choices=STATUS, default='Yes', verbose_name='Статусы')
    qr_code = models.ImageField(upload_to='images/Product/Qr_Code', blank=True, verbose_name='QR код')
    code = models.CharField(max_length=1000, blank=True, null=True, unique=True, verbose_name='Код')
    create_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        code = self.code
        if not code:
            code = get_random_string(8).upper()
        while Product.objects.filter(code=code).exclude(pk=self.pk).exists():
            code = get_random_string(8).upper()
        self.code = code

        link = 'http://127.0.0.1:8000/product_detail/'
        qrcode_img = qrcode.make(link + self.code)
        canvas = Image.new('RGB', (330, 330), 'white')
        canvas.paste(qrcode_img)
        fname = f'{self.title}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()

        imageTemproary = Image.open(self.image).convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((800, 800))
        imageTemproaryResized.save(outputIoStream, optimize=True, format='JPEG', quality=85)
        outputIoStream.seek(0)
        self.image = InMemoryUploadedFile(outputIoStream, 'ImageField',
        "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
        sys.getsizeof(outputIoStream), None)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукт'

    def count_rate(self):
        reviews = Comment.objects.filter(product=self).aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = int(reviews["avarage"])
        return avg

    def count_product(self):
        count_product = Comment.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if count_product["count"] is not None:
            cnt = int(count_product["count"])
        return cnt


class Comment(models.Model):
    STATUS = (
        ('Yes', 'Да'),
        ('No', 'Нет'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    rate = models.IntegerField(default=1, verbose_name='Рейтинг')
    text = models.TextField(verbose_name='Комментарий')
    status = models.CharField(max_length=15, choices=STATUS, default='Yes', verbose_name='Статусы')
    create_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'


class Product_Elements(models.Model):
    STATUS = (
        ('Yes', 'Да'),
        ('No', 'Нет'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    color = ColorField(verbose_name='Цвет')
    image = models.ImageField(upload_to='images/Product_Elements', blank=True, null=True, verbose_name='Изображение',
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', ])],)
    status = models.CharField(max_length=15, choices=STATUS, default='Yes', verbose_name='Статусы')
    create_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'Элементы продукта'
        verbose_name_plural = 'Элементы продукта'

    def save(self, *args, **kwargs):
        if self.image:
            imageTemproary = Image.open(self.image).convert('RGB')
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize((800, 800))
            imageTemproaryResized.save(outputIoStream, optimize=True, format='JPEG', quality=85)
            outputIoStream.seek(0)
            self.image = InMemoryUploadedFile(outputIoStream, 'ImageField',
            "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
            sys.getsizeof(outputIoStream), None)
            super(Product_Elements, self).save(*args, **kwargs)
        else:
            super(Product_Elements, self).save(*args, **kwargs)


class Faq(models.Model):
    STATUS = (
        ('Yes', 'Да'),
        ('No', 'Нет'),
    )
    question = models.CharField(max_length=100, verbose_name='Вопрос')
    response = RichTextUploadingField(verbose_name='Ответ')
    status = models.CharField(max_length=15, choices=STATUS, default='Yes', verbose_name='Статусы')
    create_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Часто задаваемые вопросы'
        verbose_name_plural = 'Часто задаваемые вопросы'


class ContactUs(models.Model):
    STATUS = (
        ('Yes', 'Да'),
        ('No', 'Нет'),
    )
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    messages = models.TextField(verbose_name='Сообщения')
    status = models.CharField(max_length=15, choices=STATUS, default='Yes', verbose_name='Статусы')
    create_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Связаться с нами'
        verbose_name_plural = 'Связаться с нами'

class News(models.Model):
    STATUS = (
        ('Yes', 'Да'),
        ('No', 'Нет'),
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(upload_to='images/News', blank=True, null=True, verbose_name='Изображение',
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', ])], )
    short_description = models.TextField(verbose_name='Краткое описание')
    description = RichTextUploadingField(verbose_name='Описание')
    status = models.CharField(max_length=15, choices=STATUS, default='Yes', verbose_name='Статусы')
    code = models.CharField(max_length=1000, blank=True, null=True, unique=True, verbose_name='Код')
    create_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

    def save(self, *args, **kwargs):
        code = self.code
        if not code:
            code = get_random_string(8).upper()
        while News.objects.filter(code=code).exclude(pk=self.pk).exists():
            code = get_random_string(8).upper()
        self.code = code
        imageTemproary = Image.open(self.image).convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1242, 537))
        imageTemproaryResized.save(outputIoStream, optimize=True, format='JPEG', quality=100)
        outputIoStream.seek(0)
        self.image = InMemoryUploadedFile(outputIoStream, 'ImageField',
        "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
        sys.getsizeof(outputIoStream), None)
        super(News, self).save(*args, **kwargs)


    def count_news_rate(self):
        reviews = News_comment.objects.filter(news=self).aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = int(reviews["avarage"])
        return avg

    def count_news(self):
        count_product = News_comment.objects.filter(news=self).aggregate(count=Count('id'))
        cnt = 0
        if count_product["count"] is not None:
            cnt = int(count_product["count"])
        return cnt


class News_comment(models.Model):
    STATUS = (
        ('Yes', 'Да'),
        ('No', 'Нет'),
    )
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новости')
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    rate = models.IntegerField(default=1, verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий')
    status = models.CharField(max_length=15, choices=STATUS, default='Yes', verbose_name='Статусы')
    create_at = models.DateField(auto_now=True, verbose_name='Создать в')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комментарий к новости'
        verbose_name_plural = 'Комментарий к новости'


class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255)
    total_price = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def client_full_name(self):
        return self.user.full_name.upper()

    @property
    def client_total_price(self):
        return self.user.total_price

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиент'

class Code(models.Model):
    number = models.CharField(max_length=6, blank=True, verbose_name='Номер')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []
        for i in range(6):
            num = random.choice(number_list)
            code_items.append(num)
            code_string = ''.join(str(item) for item in code_items)
            self.number = code_string
        super().save(*args, **kwargs)

    @property
    def client_full_name(self):
        return self.user.full_name.upper()

    class Meta:
        verbose_name = 'Коды'
        verbose_name_plural = 'Коды'

class Shopcart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    color = ColorField(verbose_name='Цвет')
    quantity = models.IntegerField(verbose_name='Количество')
    create_at = models.DateField(auto_now=True)

    def calculate_total_price(self):
        return self.product.new_price * self.quantity

    @property
    def client_full_name(self):
        return self.client.user.full_name.upper()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    color = ColorField(verbose_name='Цвет')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    country = models.CharField(max_length=255, verbose_name='Страна')
    city = models.CharField(max_length=255, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    zip_code = models.IntegerField(default=0, verbose_name='Почтовый индекс')
    order_note = models.TextField(verbose_name='Примечание к заказу')
    code = models.CharField(max_length=1000, blank=True, null=True, unique=True, verbose_name='Код')
    one_id = models.CharField(max_length=300, null=False, unique=True, blank=True, verbose_name='Один идентификатор')
    total_price = models.IntegerField(default=0, verbose_name='Общие цены')
    qr_code = models.ImageField(upload_to='images/Order/Qr_Code', blank=True, verbose_name='QR код')
    create_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        code = self.code
        if not code:
            code = get_random_string(8).upper()
        while Order.objects.filter(code=code).exclude(pk=self.pk).exists():
            code = get_random_string(8).upper()
        self.code = code

        link = 'http://127.0.0.1:8000/'
        qrcode_img = qrcode.make(link + self.one_id)
        canvas = Image.new('RGB', (330, 330), 'white')
        canvas.paste(qrcode_img)
        fname = f'{self.last_name}-{self.first_name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super(Order, self).save(*args, **kwargs)

        if not self.one_id:
            self.one_id = str(self.id)
            self.save()

    @property
    def client_full_name(self):
        return self.client.user.full_name.upper()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказ'