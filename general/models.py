from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

from utils.slugger import slugify


class Country(models.Model):
    code = models.CharField(_("Код страны"), max_length=10, unique=True)
    name = models.CharField(_("Название страны"), max_length=250)

    def __str__(self) -> str: return self.name

    class Meta:
        verbose_name = _("Страна")
        verbose_name_plural = _("Страны")


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self): return self.name


class Region(models.Model):
    name = models.CharField(_("Название региона"), max_length=100)
    country = models.ForeignKey(Country,
                                verbose_name=_("Страна"),
                                related_name="country",
                                on_delete=models.CASCADE)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")


class Sections(models.Model):
    name = models.CharField(_('Название'), max_length=255)
    icon = models.TextField(_('Путь к значку'), null=True)
    order = models.PositiveIntegerField(_('Порядок'), unique=True, null=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Раздел")
        verbose_name_plural = _("Разделы")


class Categorization(models.Model):
    name = models.CharField(_("Имя"), max_length=255)
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Родительская категория"),
        blank=True,
        null=True,
        related_name="sub_categories",
        on_delete=models.CASCADE,
    )
    section = models.ForeignKey(Sections, verbose_name=_(
        'Раздел'), related_name='section_category', on_delete=models.DO_NOTHING, null=True)

    order = models.PositiveIntegerField(_('Порядок'), unique=True, null=True)
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )

    def __str__(self) -> str: return f"{self.section}/{self.name}"

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)
        return super().save()

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


class Categories(models.Model):
    name = models.CharField(_("Название жанра"), max_length=100, unique=True)
    content = models.TextField(_("Описание жанра"), null=True)
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Родительский жанр"),
        blank=True,
        null=True,
        related_name="sub_categories",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )
    image = models.ImageField(default="art_logo.jpg")

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)
        return super().save()

    def __str__(self) -> str: return self.name

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")


class About(models.Model):
    title = models.CharField("Заголовок", max_length=255, null=True)
    text = RichTextUploadingField(_("Текст"), null=True)
    photo = models.ImageField(_("Фото"), upload_to="about/", null=True, blank=True)
    # ceo = models.CharField(_("Директор"), max_length=255,
    #                        null=True, blank=False)
    # departments = models.JSONField(_("Департаменты"), default=dict)
    # team = models.JSONField(_("Команда"), default=dict)
    # vacancies = models.JSONField(_("Вакансии"), default=dict)
    # press = models.JSONField(_("Пресса"), default=dict)
    order = models.PositiveIntegerField(_('Порядок'), unique=True, null=True)

    def __str__(self) -> str: return self.title

    class Meta:
        verbose_name = _("О нас")
        verbose_name_plural = _("О нас")


class WorkType(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    description = models.TextField(_("Описание"), max_length=5000, null=True, blank=True)
    image = models.ImageField(_("Фото"), default="art_logo.jpg")

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Вид")
        verbose_name_plural = _("Виды")


class Type(models.Model):
    name = models.CharField(_("Название"), max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Тип")
        verbose_name_plural = _("Типы")


class School(models.Model):
    name = models.CharField(_("Название"), max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Центр/школа")
        verbose_name_plural = _("Центр/школы")


class Flow(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    category = models.ForeignKey(Categorization, verbose_name=_(
        "Категория"), related_name="category_flow", null=True, on_delete=models.CASCADE)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Течение")
        verbose_name_plural = _("Течении")


class Period(models.Model):
    name = models.CharField(_("Название"), max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Период")
        verbose_name_plural = _("Периоды")


class Seller(models.Model):
    name = models.CharField(_("Название"), max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("продавец")
        verbose_name_plural = _("продавцы")


class Services(models.Model):
    name = models.CharField("Имя", max_length=255)
    content = RichTextUploadingField(_("Текст"))
    image = models.ImageField(_("Фото"), null=True, blank=True)
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )
    price = models.FloatField(_("Цена"), null=True, blank=True)
    order = models.PositiveIntegerField(_('Порядок'), unique=True, null=True)
    show_images = models.BooleanField(_('Показать картины'), default=False)

    def __str__(self) -> str: return self.name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)
        return super().save()

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")


class ServicesImage(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    images = models.ImageField(blank=True, null=True, upload_to='services/')

    def __str__(self): return self.service.name

    class Meta:
        verbose_name = _("Картинка в сервисах")
        verbose_name_plural = _("Картинки в сервисах")


class Tags(models.Model):
    name = models.CharField(_("Название"), max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")


class Sell(models.Model):
    section = models.CharField(max_length=100)
    view = models.ImageField(upload_to="requests/")
    genre = models.CharField(max_length=150)
    style = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    date = models.DateField(null=True, blank=True)
    period = models.CharField(max_length=150, null=True, blank=True)
    materials = models.CharField(max_length=150, null=True, blank=True)
    size = models.CharField(max_length=150)
    design = models.CharField(max_length=150, null=True, blank=True)
    condition = models.CharField(max_length=150)
    price = models.FloatField()
    currency = models.CharField(max_length=50)
    seller = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Запрос на продажу")
        verbose_name_plural = _("Запросы на продажу")


class TeamMember(models.Model):
    name = models.CharField(_("Имя"), max_length=100)
    photo = models.ImageField(upload_to="team/")
    description = models.TextField(_("Описание члена команды"))
    is_expert = models.BooleanField(_("Эксперт"), default=False)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Член команды")
        verbose_name_plural = _("Члены команды")


class ExpertMember(models.Model):
    name = models.CharField(_('Имя'), max_length=128)
    photo = models.ImageField(upload_to='expert/')
    certificate = models.ImageField(_('Сертификат'), upload_to='expert/certificate/', blank=True)
    description = models.TextField(_('Описание'))
    order_number = models.PositiveIntegerField(_('Порядковый номер'), unique=True, null=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _('Эксперт')
        verbose_name_plural = _('Эксперты')


class TeamMemberExtra(models.Model):
    name = models.CharField(_('Имя'), max_length=256)
    photo = models.ImageField(upload_to='team_members_extra/')
    certificate = models.ImageField(_('Сертификат'), upload_to='team_member_extra/certificate/', blank=True)
    description = models.TextField(_('Описание'))
    order_number = models.PositiveIntegerField(_('Порядковый номер'), unique=True, null=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _('Наша команда')
        verbose_name_plural = _("Наша команда")


class Dimensions(models.Model):
    name = models.CharField(_("Система измерения"), max_length=100)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _("Система измерения")
        verbose_name_plural = _("Системы измерения")


class Partner(models.Model):
    name = models.CharField(_('Название'), max_length=512)
    logo = models.ImageField(_('Логотип'), upload_to='partners/')
    description = models.TextField(_('Описание'))
    order_number = models.PositiveIntegerField(_('Порядковый номер'), unique=True, null=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _('Партнер')
        verbose_name_plural = _('Партнеры')


class AacMember(models.Model):
    name = models.CharField(_('ФИО'), max_length=512)
    photo = models.ImageField(_('Фотография'), upload_to='aac/members/')
    description = models.TextField(_('Описание'))
    certificate = models.ImageField(_('Сертификат'), upload_to='aac/certificate/', blank=True)
    order_number = models.PositiveIntegerField(_('Порядковый номер'), unique=True, null=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _('Участник команды Art Appraisal Center')
        verbose_name_plural = _('Участники команды Art Appraisal Center')


class Aac(models.Model):
    title = models.CharField(_('Заголовок'), max_length=256)
    logo = models.ImageField(_('Логотип'), upload_to='aac/')
    description = models.TextField(_('Описание'))
    certificate = models.ImageField(_('Сертификат'), upload_to='aac/')
    bottom_text = models.TextField(_('Нижний текст'), blank=True)

    def __str__(self): return self.title

    class Meta:
        verbose_name = _('Страница Art Appraisal Center')


class Aocv(models.Model):
    title = models.CharField(_('Заголовок'), max_length=256)
    text = models.TextField(_('Описание'))
    image = models.ImageField(_('Изображение'), upload_to='aocv/')

    def __str__(self): return self.title

    class Meta:
        verbose_name = _('Страница Оценка культурных ценностей')


class AocvMember(models.Model):
    name = models.CharField(_('ФИО'), max_length=128)
    photo = models.ImageField(_('Фотография'), upload_to='aocv/members/')
    text = models.TextField(_('Описание'))
    order_number = models.PositiveIntegerField(_('Порядковый номер'), unique=True, null=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = _('Участник Оценки культурных ценностей')
        verbose_name_plural = _('Участники Оценки культурных ценностей')


class AuctionRules(models.Model):
    content = RichTextUploadingField(_('Контент'))

    class Meta:
        verbose_name = _('Правила аукциона')
        verbose_name_plural = _('Правила аукциона')


class Auction(models.Model):
    name = models.CharField(_('Название аукциона'), max_length=512)
    photo = models.ImageField(_('Фотография'), upload_to='auctions/')
    date = models.DateField(_('Дата'))
    adress = models.TextField(_('Адрес проведения'))
    count_lots = models.IntegerField(_('Количество лотов'))
    assessed_value = models.FloatField(_('Оценочная стоимость'), null=True, blank=True)
    start_price_lot = models.FloatField(_('Стартовая стоимость'), null=True, blank=True)
    lot_selling_price = models.FloatField(_('Цена продажи'), null=True, blank=True)
    map = models.CharField(_('Карта'), max_length=9000, blank=True)
    content = RichTextUploadingField(_('Контент'), blank=True)
    slug = models.SlugField(
        "Дополнение к названию ссылки (генерируется автоматически)",
        default="no-slug",
        blank=True,
    )

    def __str__(self): return self.name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "no-slug" or self.slug == '':
            self.slug = slugify(self.name)
        return super().save()

    class Meta:
        verbose_name = _('Аукцион')
        verbose_name_plural = _('Аукционы')
