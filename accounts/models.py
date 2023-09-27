import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin

from utils.slugger import slugify
from utils.image_utils import image_compress
from general.models import Country, City, Categories, Categorization, Flow


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **kwargs):
        if not email:
            raise ValueError("User must have an email address")

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            last_login=now,
            date_joined=now,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        return self._create_user(email, password, False, False, **kwargs)

    def create_staffuser(self, email, password, **kwargs):
        return self._create_user(email, password, True, False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, True, True, **kwargs)


class CurrencyChoices(models.TextChoices):
    CURRENCY_USD = '$', _("Доллар США")
    CURRENCY_CNY = '¥', _("Китайский Юань")
    CURRENCY_RUB = '₽', _("Российский Рубль")
    CURRENCY_UZS = 'UZS', _("Узбекский Сум")


DEFAULT_YEAR = datetime.date.today().year - 20
YEAR_CHOICES = [(r, r) for r in range(1950, DEFAULT_YEAR)]


class AuthUsers(AbstractUser, PermissionsMixin):
    email = models.EmailField(_("Эл. адрес"), max_length=255, unique=True)
    username = models.CharField(_("Ющер"), max_length=255, blank=True, null=True)
    first_name = models.CharField(_("Имя"), blank=True, null=True, max_length=255)
    last_name = models.CharField(_("Фамилия"), blank=True, null=True, max_length=255)
    phone = models.CharField(_("Номер телефона"), max_length=255, unique=True)
    birth_date = models.DateField(_('Дата рождения'), default=datetime.date(1970, 1, 1))
    socials = models.ManyToManyField("Socials", verbose_name=_("Соц. сети"), related_name="auth_user")

    currency = models.CharField(_("Валюта"), choices=CurrencyChoices.choices, default="UZS", max_length=255)
    postcode = models.CharField(_("почтовый индекс"), blank=True, null=True, max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(_("Улица/дом/квартира"), max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self): return "/users/%i/" % self.pk

    def __str__(self) -> str: return f"User: {self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")


class Authors(models.Model):
    name = models.CharField(_("Имя"), max_length=255)
    photo = models.ImageField(_("Фото"), upload_to="authors/")
    thumbnail = models.ImageField(_("Иконка генерируется автоматически"), upload_to="thumbnail/", blank=True, null=True)
    craftmanship = models.ManyToManyField("Craftmanship", verbose_name=_("Вид деятельности"), related_name="authors")
    flow = models.ForeignKey(Flow, verbose_name=_(
        "Течение"), related_name="author_flow", null=True, on_delete=models.SET_NULL, blank=True)
    occupation1 = models.ForeignKey(Categorization, verbose_name=_(
        "Занятие1"), related_name="author_occupation", null=True, blank=True, on_delete=models.CASCADE)
    contract_number = models.CharField(
        _("Номер договора"), blank=True, null=True, max_length=255
    )
    socials = models.ManyToManyField(
        "Socials", verbose_name=_("Соц. сети"), related_name="author"
    )
    occupation = models.CharField(_("Занятие"), max_length=255)
    bio = RichTextUploadingField(_("Био"))
    dob = models.IntegerField(_("Дата рождения"), null=True)
    dod = models.IntegerField(_("Дата смерти"), null=True, blank=True)
    is_organisation = models.BooleanField(_('Организация'), default=False)

    def compress_image(self, uploaded_image): image_compress(self, uploaded_image, add_watermark=False)

    def save(self, *args, **kwargs):
        if not self.photo:
            self.thumbnail = None
        else:
            self.compress_image(self.photo)
        super().save()

    def __str__(self) -> str: return self.name

    class Meta:
        verbose_name = _("Автор")
        verbose_name_plural = _("Авторы")


class SecondAuthor(models.Model):
    name = models.CharField(_("Имя"), max_length=255)
    photo = models.ImageField(_("Фото"), upload_to="authors/")
    thumbnail = models.ImageField(_("Иконка генерируется автоматически"), upload_to="thumbnail/", blank=True, null=True)
    craftmanship = models.ManyToManyField("Craftmanship", verbose_name=_("Вид деятельности"), related_name="second_authors")
    flow = models.ForeignKey(Flow, verbose_name=_(
        "Течение"), related_name="second_author_flow", null=True, on_delete=models.SET_NULL, blank=True)
    occupation1 = models.ForeignKey(Categorization, verbose_name=_(
        "Занятие1"), related_name="second_author_occupation", null=True, blank=True, on_delete=models.CASCADE)
    contract_number = models.CharField(
        _("Номер договора"), blank=True, null=True, max_length=255
    )
    socials = models.ManyToManyField(
        "Socials", verbose_name=_("Соц. сети"), related_name="second_author"
    )
    occupation = models.CharField(_("Занятие"), max_length=255)
    bio = RichTextUploadingField(_("Био"))
    dob = models.IntegerField(_("Дата рождения"), null=True)
    dod = models.IntegerField(_("Дата смерти"), null=True, blank=True)
    is_organisation = models.BooleanField(_('Организация'), default=False)

    def compress_image(self, uploaded_image): image_compress(self, uploaded_image, add_watermark=False)

    def save(self, *args, **kwargs):
        if not self.photo:
            self.thumbnail = None
        else:
            self.compress_image(self.photo)
        super().save()

    def __str__(self) -> str: return self.name

    class Meta:
        verbose_name = _("Другой Автор")
        verbose_name_plural = _("Другие Авторы")


class Craftmanship(models.Model):
    name = models.CharField(_("Имя"), max_length=255)
    category = models.ForeignKey(Categorization, verbose_name=_(
        "Занятие1"), related_name="craftmanship", null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)
        return super().save()

    class Meta:
        verbose_name = _("Ремесло")
        verbose_name_plural = _("Ремесла")


class Socials(models.Model):
    name = models.CharField(_("Название соц. сети"), max_length=200)
    social_url = models.URLField(
        _("Ссылка на соц.сеть"), max_length=250, null=True)

    def __str__(self) -> str: return f"{self.name}: {self.social_url}"

    class Meta:
        verbose_name = _("Соц.сеть")
        verbose_name_plural = _("Соц.сети")
