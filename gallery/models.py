from django.db import models
from django.contrib import admin
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

from general.models import Categories, Country, Sections, Tags, WorkType, Flow, \
    Seller, Period, Categorization, Region, Services, School, Type, Dimensions
from accounts.models import AuthUsers, Authors, SecondAuthor
from utils.image_utils import image_compress, add_photo_logo, rotate_image
from utils.slugger import slugify
from .manager import WorksManager


class StatusChoices(models.TextChoices):
    ORDERED = 'ordered', _("Заказан")
    SOLD = 'sold', _("Продано")
    NEW = 'new', _("Новый")


class OrderStatusChoices(models.TextChoices):
    ORDER_PAID = 'paid', _("Оплачено")
    ORDER_PENDING = 'pending', _("Ожидается")
    ORDER_COMPLETE = 'complete', _("Завершено")
    ORDER_CANCELED = 'canceled', _("Отменено")
    ORDER_RETURNED = 'returned', _("Возврашено")
    ORDER_REJECTED = 'rejected', _("Отклонено")


class CartItemChoices(models.TextChoices):
    CART_SOLD = 'sold', _("Продано")
    CART_CART = 'cart', _("В корзине")
    CART_PENDING = 'pending', _("Ожидается")
    CART_WISHLIST = 'wishlist', _("В избранном")


class OrderItemChoices(models.TextChoices):
    ORDER_SOLD = 'sold', _("Продано")
    ORDER_PENDING = 'pending', _("Ожидается")
    ORDER_CANCELED = 'canceled', _("Отменено")


class Works(models.Model):
    u_id = models.CharField(
        _("Уникальный артикль (генерируется автоматически)"),
        blank=True,
        null=True,
        max_length=255,
    )
    section = models.ForeignKey(Sections, verbose_name=_(
        'Oтдел'), related_name='work_section', null=True, on_delete=models.DO_NOTHING)
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True, max_length=255
    )
    author = models.ForeignKey(
        Authors,
        verbose_name=_("Автор"),
        related_name="work_author",
        on_delete=models.DO_NOTHING,
    )
    second_author = models.ForeignKey(
        SecondAuthor,
        verbose_name=_("Другой Автор"),
        related_name="work_second_author",
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    genre = models.ManyToManyField(
        Categories, verbose_name=_("жанр"), related_name="art_works"
    )
    name = models.CharField(_("Название"), max_length=255)
    description = models.TextField(_('Описание'), null=True, blank=True)
    type = models.ForeignKey(WorkType, verbose_name=_(
        'Bид'), related_name="work_type", blank=True, null=True, on_delete=models.DO_NOTHING)
    period = models.ForeignKey(Period,
                               verbose_name=_('период'), related_name="work_period", blank=True, null=True,
                               on_delete=models.DO_NOTHING)
    flow = models.ForeignKey(Flow,
                             verbose_name=_('течение'), related_name="work_flow", blank=True, null=True,
                             on_delete=models.DO_NOTHING)
    show_in_service = models.ManyToManyField(Services, verbose_name=_('сервисы'), related_name="artworks", blank=True)

    size = models.CharField(_("Размер"), max_length=255, blank=True, null=True)
    dimensions = models.ForeignKey(Dimensions,
                                   verbose_name=_("Система Исчесления"),
                                   related_name="work_dimension",
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)

    signature = models.CharField(
        _("Подпись (положение подписи)"), max_length=255, blank=True, null=True)
    age_restriction = models.BooleanField(_("Контент 16+"), default=False)
    country = models.ForeignKey(
        Country,
        verbose_name=_("Страна"),
        related_name="art_works",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    regions = models.ManyToManyField(Region, verbose_name=_(
        "Регионы"), related_name="work_regions")
    price = models.FloatField(_("Цена"), max_length=255, blank=True, null=True)
    quantity = models.IntegerField(_("Количество"), null=True)
    discount = models.OneToOneField(
        "Discounts",
        verbose_name=_("Скидка"),
        related_name="art_work",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    shoppable = models.BooleanField(_("Доступно для продажи"), default=True)
    popular = models.BooleanField(_("Популярный"), default=False, null=True)
    photo = models.ImageField(_("Изображение"), upload_to="works/")
    thumbnail = models.ImageField(_("Иконка (генерируется автоматически)"), upload_to="thumbnail/", blank=True,
                                  null=True)
    material = models.CharField(
        _("Mатериал"), max_length=255, blank=True, null=True)
    year_of_creation = models.IntegerField(
        _("Год исполнения"), null=True, blank=True)
    tags = models.ManyToManyField(Tags,
                                  verbose_name=_('Теги'), related_name='work_tags', blank=True)
    price_up = models.BooleanField(_('прайс ап'), default=False, null=True)
    seller = models.ForeignKey(Seller,
                               verbose_name=_('продавец'), related_name="work_seller", null=True, blank=True,
                               on_delete=models.DO_NOTHING)
    for_interier = models.BooleanField(
        _('для интерьера'), default=False, null=True)
    status = models.CharField(
        _("Cтатус"), choices=StatusChoices.choices, default="new", max_length=255
    )
    pub_date = models.DateTimeField(_("Дата публикации"), auto_now_add=True)
    starts_at = models.DateTimeField(
        _("Дата начала продажи"), blank=True, null=True)
    ends_at = models.DateTimeField(
        _("Дата окончания продажи"), blank=True, null=True)
    add_watermark = models.BooleanField(_("Добавить логотип"), default=False)
    objects = WorksManager()
    views = models.PositiveIntegerField(_("Просмотры"), default=0)

    @admin.display(description="Уникальный артикль")
    def uid_name(self):
        return self.u_id

    def make_uid(self):
        if self.u_id is None and self.second_author.contract_number:
            self.u_id = "{}/{}/{}".format(
                self.second_author.contract_number, str(self.second_author.id), str(self.id)
            )
        if self.u_id is None:
            self.u_id = "{}/{}/{}".format(
                self.author.contract_number, str(self.author.id), str(self.id)
            )
            self.save()

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)

        if not self.photo:
            self.thumbnail = None
        else:
            rotate_image(uploaded_image=self.photo)
            # image_compress(self, uploaded_image=self.photo, add_watermark=self.add_watermark)
            # if self.add_watermark:
            #     add_photo_logo(self)

        super().save()
        self.make_uid()
        if str(self.pk) not in self.slug:
            self.slug = f'{str(self.pk)}-{self.slug}'
            super().save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Изобразительное исскуство")
        verbose_name_plural = _("Изобразительное исскуства")


class AppliedArt(models.Model):
    u_id = models.CharField(
        _("Уникальный артикль (генерируется автоматически)"),
        blank=True,
        null=True,
        max_length=255,
    )
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True, max_length=255
    )

    vid = models.ForeignKey(WorkType, verbose_name=_('Bид'),
                            related_name="art_type", blank=True, null=True, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, verbose_name=_('Тип'),
                             related_name="applied_art_type", blank=True, null=True, on_delete=models.DO_NOTHING)
    school = models.ForeignKey(School, verbose_name=_('Центр/школа'),
                               related_name="school", blank=True, null=True, on_delete=models.DO_NOTHING)
    photo = models.ImageField(_("Изображение"), upload_to="works/")
    thumbnail = models.ImageField(_("Иконка (генерируется автоматически)"),
                                  upload_to="thumbnail/", blank=True, null=True)
    name = models.CharField(_("Название"), max_length=255)
    author = models.ForeignKey(
        Authors,
        verbose_name=_("Автор"),
        related_name="art_author",
        on_delete=models.DO_NOTHING,
    )
    year_of_creation = models.IntegerField(
        _("Год создания"), null=True, blank=True)
    period = models.ForeignKey(Period, verbose_name=_('Период'),
                               related_name="art_period", blank=True, null=True, on_delete=models.DO_NOTHING)
    description = models.TextField(_('Описание'), null=True, blank=True)
    material = models.CharField(_("Mатериал"), max_length=255, blank=True, null=True)
    size = models.CharField(_("Размер"), max_length=255, blank=True, null=True)
    dimensions = models.ForeignKey(Dimensions,
                                   verbose_name=_("Система Исчесления"),
                                   related_name="appliedart_dimension",
                                   null=True, blank=True,
                                   on_delete=models.DO_NOTHING)

    price = models.FloatField(_("Цена"), max_length=255, blank=True, null=True)
    tags = models.ManyToManyField(Tags, verbose_name=_('Теги'), related_name='art_tags', blank=True)
    country = models.ForeignKey(
        Country,
        verbose_name=_("Страна"),
        related_name="works",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    regions = models.ManyToManyField(Region, verbose_name=_("Регионы"), related_name="art_regions")
    price_up = models.BooleanField(_('Прайс ап'), default=False, null=True)
    seller = models.ForeignKey(Seller, verbose_name=_('продавец'),
                               related_name="art_seller", null=True, blank=True, on_delete=models.DO_NOTHING)
    for_interier = models.BooleanField(
        _('для интерьера'), default=False, null=True)

    age_restriction = models.BooleanField(_("Контент 16+"), default=False)
    quantity = models.IntegerField(_("Количество"), null=True)
    discount = models.OneToOneField(
        "Discounts",
        verbose_name=_("Скидка"),
        related_name="work",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    status = models.CharField(_("Cтатус"), choices=StatusChoices.choices, default="new", max_length=255)
    starts_at = models.DateTimeField(_("Дата начала продажи"), blank=True, null=True)
    ends_at = models.DateTimeField(_("Дата окончания продажи"), blank=True, null=True)
    pub_date = models.DateTimeField(_("Дата публикации"), auto_now_add=True)
    shoppable = models.BooleanField(_("Доступно для продажи"), default=True)
    popular = models.BooleanField(_("Популярный"), default=False, null=True)
    add_watermark = models.BooleanField(_("Добавить логотип"), default=False)
    objects = WorksManager()
    views = models.PositiveIntegerField(_("Просмотры"), default=0)

    @admin.display(description="Уникальный артикль")
    def uid_name(self):
        return self.u_id

    def make_uid(self):
        if self.u_id is None:
            self.u_id = "{}/{}/{}".format(
                self.author.contract_number, str(self.author.id), str(self.id)
            )
            self.save()

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)

        if not self.photo:
            self.thumbnail = None
        else:
            rotate_image(uploaded_image=self.photo)
            image_compress(self, uploaded_image=self.photo, add_watermark=self.add_watermark)
            if self.add_watermark:
                add_photo_logo(self)

        super().save()
        self.make_uid()
        if str(self.pk) not in self.slug:
            self.slug = f'{str(self.pk)}-{self.slug}'
            super().save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Прикладное искусство")
        verbose_name_plural = _("Прикладные искусства")


class Article(models.Model):
    title = models.CharField(_("Заголовок"), max_length=255, unique=True)
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )
    description = models.TextField(_("Описание"))
    image = models.ImageField(_("Фото"), upload_to="articles/", null=True, blank=True)
    text = RichTextUploadingField(_("Текст"))
    pub_date = models.DateTimeField(_("Дата публикации"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.title)
        return super().save()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Статья")
        verbose_name_plural = _("Статьи")


class Cart(models.Model):
    user = models.OneToOneField(
        AuthUsers,
        verbose_name=_("Пользователь"),
        related_name="user_basket",
        on_delete=models.CASCADE,
    )
    cart_items = models.ManyToManyField(
        "CartItem", verbose_name=_("Произведения"), related_name="cart"
    )

    def __str__(self) -> str:
        works_fetched = self.cart_items.prefetch_related()
        works_list = [str(x) for x in works_fetched]
        return f"{self.user.first_name} <-- {self.cart_items.all()}"

    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")


class CartItem(models.Model):
    art_work = models.ForeignKey(
        Works,
        verbose_name=_("Произведение"),
        related_name="cart_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    applied_art = models.ForeignKey(
        AppliedArt,
        verbose_name=_("Прикладное искусство"),
        related_name="applied_cart_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    status = models.CharField(
        _("Cтатус"), choices=CartItemChoices.choices, default="new", max_length=255
    )
    is_applied_art = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.is_applied_art:
            return f"{self.applied_art}({self.status})"
        else:
            return f"{self.art_work}({self.status})"

    class Meta:
        verbose_name = _("Продукт в корзине")
        verbose_name_plural = _("Продукты в корзине")


class Order(models.Model):
    user = models.ForeignKey(
        AuthUsers,
        verbose_name=_("Пользователь"),
        related_name="orders",
        on_delete=models.DO_NOTHING,
    )
    status = models.CharField(
        _("Статус"), max_length=255, choices=OrderStatusChoices.choices)
    sub_total = models.FloatField(_("Под итог"))
    discount = models.FloatField(_("Скидки"), null=True, blank=True)
    total = models.FloatField(_("Итого"))
    created_at = models.DateTimeField(_("Оформлено"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)
    works = models.ManyToManyField(
        "OrderItems", verbose_name=_("Произведения"), related_name="orders"
    )

    def __str__(self) -> str:
        return f"{self.user}: {self.total} -- {self.status}"

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")


class OrderItems(models.Model):
    art_work = models.ForeignKey(
        Works,
        verbose_name=_("Произведение"),
        related_name="order_items",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    applied_art = models.ForeignKey(
        AppliedArt,
        verbose_name=_("Произведение"),
        related_name="order_items",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.CharField(
        _("Cтатус"),
        choices=OrderItemChoices.choices,
        default=OrderItemChoices.ORDER_PENDING,
        max_length=255,
    )
    is_applied_art = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.art_work}({self.status})"

    class Meta:
        verbose_name = _("Продукт в заказе")
        verbose_name_plural = _("Продукты в заказе")


class Discounts(models.Model):
    amount = models.FloatField(_("Скидка"))
    starts_at = models.DateTimeField(
        _("Дата начала скидки"), auto_now_add=True, blank=True, null=True
    )
    ends_at = models.DateTimeField(
        _("Дата окончания скидки"), blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.amount}%"

    class Meta:
        verbose_name = _("Скидка")
        verbose_name_plural = _("Скидки")


class ProductReview(models.Model):
    art_work = models.ForeignKey(
        Works,
        verbose_name=_("Произведение"),
        related_name="review",
        on_delete=models.CASCADE,
    )
    parent_id = models.ForeignKey(
        "self",
        verbose_name=_("Родительский обзор"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user_id = models.ForeignKey(
        AuthUsers, verbose_name=_("Пользователь"), on_delete=models.CASCADE
    )
    rating = models.FloatField(_("Оценка"))
    content = models.TextField(_("Обзор"), null=True)
    published = models.BooleanField(_("Виден"), default=True)
    created_at = models.DateTimeField(_("Дата обзора"), auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.art_work}: {self.content}. {self.rating}"

    class Meta:
        verbose_name = _("Обзор")
        verbose_name_plural = _("Обзоры")


class Likes(models.Model):
    user = models.ForeignKey(
        AuthUsers,
        verbose_name=_("Пользователь"),
        related_name="liked",
        on_delete=models.CASCADE,
    )
    art_work = models.ForeignKey(
        Works,
        verbose_name=_("Произведение"),
        related_name="liked",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата изменения"), auto_now=True)

    def __str__(self) -> str:
        return f"{self.user}: {self.art_work}"

    class Meta:
        verbose_name = _("Лайк")
        verbose_name_plural = _("Лайки")


class Gallery(models.Model):
    photo = models.ImageField(_("Фото"), upload_to="works/gallery/", null=True)
    work = models.ForeignKey(
        Works,
        verbose_name=_("Произведение"),
        related_name="work_gallery",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Галерея")
        verbose_name_plural = _("Галереи")


class Auctions(models.Model):
    name = models.CharField("Имя", max_length=255)
    product = models.OneToOneField(
        Works,
        verbose_name=_("Предмет Искусства"),
        null=True,
        related_name="auction",
        on_delete=models.SET_NULL,
    )
    current_price = models.FloatField()
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )
    winner_user = models.ForeignKey(AuthUsers,
                                    verbose_name=_("Победитель аукциона"),
                                    related_name="auction",
                                    on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(AuthUsers, verbose_name=_(
        "Участники аукциона"), related_name="auctions", blank=True)
    date_of_start = models.DateField(_('Дата начала'))
    date_of_end = models.DateField(_('Дата окончания'))

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)
        return super().save()

    class Meta:
        verbose_name = _("Аукцион")
        verbose_name_plural = _("Аукционы")


class WorkPriceUp(models.Model):
    name = models.CharField("Имя", max_length=255)
    product = models.OneToOneField(
        Works,
        verbose_name=_("Предмет Искусства"),
        null=True,
        related_name="work_price_up_auction",
        on_delete=models.SET_NULL,
    )
    current_price = models.FloatField()
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )
    winner_user = models.ForeignKey(AuthUsers,
                                    verbose_name=_("Победитель прайс ап"),
                                    related_name="work_price_up_winner",
                                    on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(AuthUsers, verbose_name=_(
        "Участники прайс ап"), related_name="work_price_up_participants", blank=True)
    date_of_start = models.DateField(_('Дата начала'))
    date_of_end = models.DateField(_('Дата окончания'))

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)
        return super().save()

    class Meta:
        verbose_name = _("Прайс ап")
        verbose_name_plural = _("Прайс ап")


class AppliedArtPriceUp(models.Model):
    name = models.CharField("Имя", max_length=255)
    product = models.OneToOneField(
        AppliedArt,
        verbose_name=_("Прикладные искусства"),
        null=True,
        related_name="applied_art_price_up_auction",
        on_delete=models.SET_NULL,
    )
    current_price = models.FloatField()
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )
    winner_user = models.ForeignKey(AuthUsers,
                                    verbose_name=_("Победитель прайс ап"),
                                    related_name="appliedart_price_up_winner",
                                    on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(AuthUsers, verbose_name=_(
        "Участники прайс ап"), related_name="appliedart_price_up_participants", blank=True)
    date_of_start = models.DateField(_('Дата начала'))
    date_of_end = models.DateField(_('Дата окончания'))

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)
        return super().save()

    class Meta:
        verbose_name = _("Прайс ап")
        verbose_name_plural = _("Прайс ап")


class Views(models.Model):
    art_work = models.ForeignKey(
        Works,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='work_views'
    )
    applied_art = models.ForeignKey(
        AppliedArt,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='applied_art_views'
    )
    views = models.PositiveIntegerField(default=0)
    is_applied_art = models.BooleanField(default=False)

    def __str__(self): return 'Views Count'

    class Meta:
        verbose_name = _("Количество просмотров")
        verbose_name_plural = _("Количество просмотров")
