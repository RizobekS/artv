from functools import reduce
from itertools import chain
import operator
import random
import datetime

from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required


from general import filters
from utils.currency_utils import get_currencies
from utils.cart_utils import get_cart_items_count
from utils.models_utils import get_valid_craftmanship
from utils.get_common_context import get_common_context
from utils.network_utils import client_country, get_ip
from accounts.models import Authors, AuthUsers, Craftmanship
from utils import currency_change_utils, age_restriction_utils
from accounts.forms import UpdateCheckoutProfileForm, UpdateProfileForm
from gallery.models import Article, Auctions, Works, Gallery, CartItem, CartItemChoices, Order, Cart, \
    StatusChoices, AppliedArt, Views
from .models import Country, Categories, About, Flow, Region, Services, Sections, WorkType, Sell, TeamMember, \
    ServicesImage, ExpertMember, Partner, Aac, AacMember, Aocv, AocvMember, TeamMemberExtra, AuctionRules, Auction, \
    Lots, PublishHouseArt, PublishHouseWork


def error_404_view(request, exception):
    template_name = "pages/e404.html"
    return render(request, template_name)


class Home(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self):
        ip = get_ip(request=self.request)
        applied_work = age_restriction_utils.get_safe_works(self.request, applied_art=True).order_by("-pub_date")
        all_work = age_restriction_utils.get_safe_works(self.request).order_by("-pub_date")
        most_visited = age_restriction_utils.get_safe_works(self.request).order_by("-views")
        articles = Article.objects.all().order_by("-pub_date")[:3]
        services = Services.objects.all().order_by("order")
        cart_items = get_cart_items_count(self.request.user)
        sections = Sections.objects.all().order_by("order")
        abouts = About.objects.all().order_by("order")
        country_code, country_name = client_country(ip)
        craftmanship = get_valid_craftmanship()
        categories = Categories.objects.all()
        currencies = get_currencies()
        works_by_section = []
        new_sections = []
        izo_work = []

        for section in sections:
            if not section.work_section.exists():
                section.valid = False
            else:
                section.valid = True
                work = all_work.filter(section=section).first()
                works_by_section.append(work)

            new_sections.append(section)
            if section.id == 1:
                izo_work = all_work.filter(section=section)

        common_context = get_common_context(self.request, work=all_work)
        rand_works = random.sample(list(all_work), 12)
        works_by_section = works_by_section[:8]
        applied_work = list(applied_work)[:8]
        most_visited = list(most_visited)[:6]
        rand_works = list(rand_works)[:12]
        izo_work = list(izo_work)[:8]

        context = {
            **common_context,
            "works_for_section": works_by_section,
            "country_name": country_name,
            "craftmanship": craftmanship,
            "applied_work": applied_work,
            "most_visited": most_visited,
            "sections": set(sections),
            "rand_works": rand_works,
            "cart_items": cart_items,
            "currencies": currencies,
            "categories": categories,
            "servicesy": services,
            "articles": articles,
            "izo_work": izo_work,
            "works": all_work,
            "abouty": abouts,
        }

        return context


class Catalog(TemplateView):
    template_name = "pages/catalog.html"

    def get_context_data(self):
        countries = Country.objects.all()
        categories = Categories.objects.all()
        works = age_restriction_utils.get_safe_works(self.request).order_by("-price")

        common_context = get_common_context(self.request)

        q = Q()

        if self.request.GET.get("price"):
            price = self.request.GET.get("price")
            if price == "desc":
                works = works.order_by("price")
        if self.request.GET.get("country"):
            country = self.request.GET.get("country")
            q |= Q(country__name=country)
        if self.request.GET.get("category"):
            cat = self.request.GET.get("category")
            q |= Q(work_article__category__name=cat)

        if self.request.GET.get("search"):
            key = self.request.GET.get("search")
            works = works.filter(name__icontains=key)

        works = works.filter(q)

        context = {
            "categories": categories, **common_context,
            "works": works, "countries": countries
        }

        return context


def catalog_detail(request, slug):
    template_name = "pages/catalog-detail.html"

    work = price = currency = galleries = other_works = status = None

    if Works.objects.filter(slug=slug).exists():
        work = age_restriction_utils.get_safe_works(request).get(slug=slug)
        other_works = age_restriction_utils.get_safe_works(request).exclude(id=work.id)
        currency, price = currency_change_utils.user_currency(request, price=work.price)
        galleries = Gallery.objects.filter(work=work.id)

        work.views += 1
        work.save()

    elif AppliedArt.objects.filter(slug=slug).exists():
        work = age_restriction_utils.get_safe_works(request, applied_art=True).get(slug=slug)
        other_works = age_restriction_utils.get_safe_works(request, applied_art=True).exclude(id=work.id)
        currency, price = currency_change_utils.user_currency(request, price=work.price)
        galleries = Gallery.objects.filter(work=work.id)

        work.views += 1
        work.save()

    common_context = get_common_context(request, work=work)
    regions = []
    regions_str = ""

    if work:
        for region in work.regions.all():
            regions.append(region.name)
        if len(regions) > 1:
            regions_str = ", ".join(regions)

    material = None
    if not work.material == "-- sorry, no translation provided --":
        material = work.material

    if work.status == 'sold' or work.status == 'ordered':
        status = 'sold'

    other_works = random.sample(list(other_works), 8)

    context = {
        **common_context,
        'url': f"{request.get_host()}{reverse('home_page')}catalog/{work.slug}/",
        "price": price, "currency": currency,
        "work": work, "material": material,
        "other_works": other_works,
        "galleries": galleries,
        "regions": regions_str,
        "status": status,
    }
    return render(request, template_name, context)


class Blog(TemplateView):
    template_name = "pages/blog.html"

    def get_context_data(self):
        articles = Article.objects.all().order_by("-pub_date")
        if articles.count() > 3:
            article_main = articles[:3]
            articles = articles[3:]
        else:
            article_main = articles[:1]
            articles = articles[1:]
        common_context = get_common_context(self.request)

        # for article in articles:
        #     if article_main:
        #         articles = articles.exclude(id=article.id)

        context = {
            **common_context,
            "articles": articles,
            "mains": article_main,
        }
        return context


class BlogDetail(DetailView):
    template_name = "pages/blog-detail.html"
    model = Article

    def get_context_data(self, **kwargs):
        obj = super().get_object()
        article = Article.objects.get(id=obj.id)
        other_articles = Article.objects.all().exclude(id=article.id)[:3]
        common_context = get_common_context(self.request)
        context = {
            **common_context,
            "others": other_articles,
            "article": article
        }
        return context


class Auctions(TemplateView):
    template_name = "pages/auctions.html"
    model = Auctions

    def get_context_data(self):
        auctions = Auction.objects.all()
        common_context = get_common_context(self.request)
        context = {
            **common_context,
            "auctions": auctions,
        }
        return context


# class AuctionDetail(TemplateView):
#     template_name = "pages/auction-detail.html"
#
#     def get_context_data(self):
#         obj = super().get_object()
#         auction = Auction.objects.get(id=obj)
#
#         common_context = get_common_context(self.request)
#         context = {
#             **common_context,
#             "auction": auction,
#         }
#         return context


def gallery_details(request, pk=None):
    template_name = "pages/gallery-detail.html"
    if pk:
        context = {
            'pk': pk
        }
        return render(request, template_name, context)
    return render(request, template_name)


def gallery_applied_art_api(request, pk=2):
    ip = get_ip(request=request)
    country_code, country_name = client_country(ip)
    # paginating works and if, else part is for the filter
    page_number = request.GET.get("page", 1)
    applied_art = age_restriction_utils.get_safe_works(request, applied_art=True)
    cart_items = get_cart_items_count(request.user)


    # filter
    if request.GET.get("regions"):
        _id = request.GET["regions"]
        applied_art = age_restriction_utils.get_safe_works(request, obj=applied_art)
        applied_art = applied_art.filter(regions__id=_id).order_by("-pub_date")

    if request.GET.get("authors"):
        _id = request.GET["authors"]
        applied_art = age_restriction_utils.get_safe_works(request, obj=applied_art)
        applied_art = applied_art.filter(author__id=_id).order_by("-pub_date")

    if request.GET.get("types"):
        _id = request.GET["types"]
        applied_art = age_restriction_utils.get_safe_works(request, obj=applied_art)
        applied_art = applied_art.filter(type__id=_id).order_by("-pub_date")

    if request.GET.get("classes"):
        _id = request.GET["classes"]
        applied_art = age_restriction_utils.get_safe_works(request, obj=applied_art)
        applied_art = applied_art.filter(vid__id=_id).order_by("-pub_date")


    paginator = Paginator(applied_art, 6)
    page_obj = paginator.get_page(page_number)

    # obtaining specific types, authors, regions that are related only with AppliedArt model
    abouts = About.objects.all()
    services = Services.objects.all()
    sections = Sections.objects.all()
    craftsmanships = Craftmanship.objects.all()
    types_list = applied_art.values_list('type__id', flat=True).distinct()
    types = WorkType.objects.filter(reduce(operator.or_, (Q(id=i) for i in types_list)))
    classes_list = applied_art.values_list('vid_id', flat=True).distinct()
    classes = WorkType.objects.filter(reduce(operator.or_, (Q(id=i) for i in classes_list)))
    authors_list = applied_art.values_list('author__id', flat=True).distinct()
    authors = Authors.objects.filter(reduce(operator.or_, (Q(id=i) for i in authors_list)))
    regions_list = applied_art.values_list('regions__id', flat=True).distinct()
    regions = Region.objects.filter(reduce(operator.or_, (Q(id=i) for i in regions_list)))

    # preparing data to be sent and localization
    regions_dict = {"name": [region.name for region in regions], "id": [region.id for region in regions]}
    if get_language() == "en":
        types_dict = [
            {'id': _type.id,
             'name': _type.name_en if _type.name_en else _type.name}
            for _type in types
        ]
        authors_dict = [
            {'id': author.id,
             'name': author.name_en if author.name_en else author.name}
            for author in authors
        ]
        sections_dict = [
            {'id': section.id,
             'name': section.name_en if section.name_en else section.name,
             'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'url-api': f"{request.get_host()}{reverse('home_page')}gallery-api/{section.id}",
             }
            for section in sections
        ]
        classes_dict = [
            {'id': _type.id,
             'name': _type.name_en if _type.name_en else _type.name}
            for _type in classes
        ]

        data_dict = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'name': kw.name_en if kw.name_en else kw.name,
             'status': kw.status_en if kw.status_en else kw.status,
             'author': kw.author.name_en if kw.author.name_en else kw.author.name,
             'country': kw.country.name_en if kw.country.name_en else kw.country.name}
            for kw in page_obj.object_list
        ]
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_en if about.title_en else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': 'Our Team'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': 'Experts'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_en if service.name_en else service.name}
            for service in services
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_en if craftsmanship.name_en else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]

    elif get_language() == "uz":
        types_dict = [
            {'id': _type.id,
             'name': _type.name_uz if _type.name_uz else _type.name}
            for _type in types
        ]
        authors_dict = [
            {'id': author.id,
             'name': author.name_uz if author.name_uz else author.name}
            for author in authors
        ]
        sections_dict = [
            {'id': section.id,
             'name': section.name_uz if section.name_uz else section.name,
             'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'url-api': f"{request.get_host()}{reverse('home_page')}gallery-api/{section.id}",
             }
            for section in sections
        ]
        classes_dict = [
            {'id': _type.id,
             'name': _type.name_uz if _type.name_uz else _type.name}
            for _type in classes
        ]

        data_dict = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'name': kw.name_uz if kw.name_uz else kw.name,
             'status': kw.status_uz if kw.status_uz else kw.status,
             'author': kw.author.name_uz if kw.author.name_uz else kw.author.name,
             'country': kw.country.name_uz if kw.country.name_uz else kw.country.name}
            for kw in page_obj.object_list
        ]
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_uz if about.title_uz else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': 'Bizning Jamoa'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': 'Ekspertlar'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_uz if service.name_uz else service.name}
            for service in services
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_uz if craftsmanship.name_uz else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]

    elif get_language() == "zh_cn":
        types_dict = [
            {'id': _type.id,
             'name': _type.name_zh_cn if _type.name_zh_cn else _type.name}
            for _type in types
        ]
        authors_dict = [
            {'id': author.id,
             'name': author.name_zh_cn if author.name_zh_cn else author.name}
            for author in authors
        ]
        sections_dict = [
            {'id': section.id,
             'name': section.name_zh_cn if section.name_zh_cn else section.name,
             'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'url-api': f"{request.get_host()}{reverse('home_page')}gallery-api/{section.id}",
             }
            for section in sections
        ]
        classes_dict = [
            {'id': _type.id,
             'name': _type.name_zh_cn if _type.name_zh_cn else _type.name}
            for _type in classes
        ]

        data_dict = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'name': kw.name_zh_cn if kw.name_zh_cn else kw.name,
             'status': kw.status_zh_cn if kw.status_zh_cn else kw.status,
             'author': kw.author.name_zh_cn if kw.author.name_zh_cn else kw.author.name,
             'country': kw.country.name_zh_cn if kw.country.name_zh_cn else kw.country.name}
            for kw in page_obj.object_list
        ]
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_zh_cn if about.title_zh_cn else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': '我們的隊伍'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': '專家'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_zh_cn if service.name_zh_cn else service.name}
            for service in services
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_zh_cn if craftsmanship.name_zh_cn else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]

    else:
        types_dict = [
            {'id': _type.id,
             'name': _type.name_ru if _type.name_ru else _type.name}
            for _type in types
        ]
        authors_dict = [
            {'id': author.id,
             'name': author.name_ru if author.name_ru else author.name}
            for author in authors
        ]
        sections_dict = [
            {'id': section.id,
             'name': section.name_ru if section.name_ru else section.name,
             'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'url-api': f"{request.get_host()}{reverse('home_page')}gallery-api/{section.id}",
             }
            for section in sections
        ]
        classes_dict = [
            {'id': _type.id,
             'name': _type.name_ru if _type.name_ru else _type.name}
            for _type in classes
        ]

        data_dict = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'name': kw.name_ru if kw.name_ru else kw.name,
             'status': kw.status_ru if kw.status_ru else kw.status,
             'author': kw.author.name_ru if kw.author.name_ru else kw.author.name,
             'country': kw.country.name_ru if kw.country.name_ru else kw.country.name}
            for kw in page_obj.object_list
        ]
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_ru if about.title_ru else about.title}
            for about in abouts]
        our_team = {
            'url': f"{request.get_host()}{reverse('home_page')}about/team",
            'name': 'Наша команда'}
        experts = {
            'url': f"{request.get_host()}{reverse('home_page')}about/experts",
            'name': 'Эксперты'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_ru if service.name_ru else service.name}
            for service in services
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_ru if craftsmanship.name_ru else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]
    abouts.append(experts)
    abouts.append(our_team)

    # context data for sending
    context = {
        "applied_art_activated": False,
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data_dict,
        "types": types_dict,
        "lang": get_language(),
        "classes": classes_dict,
        "regions": regions_dict,
        "authors": authors_dict,
        "sections": sections_dict,
        "cart_items": cart_items,

        'craftsmanships': craftsmanships,
        "country_name": country_name,
        'services': services,
        'abouts': abouts

    }
    return JsonResponse(context)


def gallery_details_api(request, pk=None):
    ip = get_ip(request=request)
    country_code, country_name = client_country(ip)


    # sending flows, types, authors, genres, regions for the filter
    flows = Flow.objects.all()
    abouts = About.objects.all()
    regions = Region.objects.all()
    types = WorkType.objects.all()
    authors = Authors.objects.all()
    services = Services.objects.all()
    genres = Categories.objects.all()
    sections = Sections.objects.all()
    craftsmanships = Craftmanship.objects.all()
    cart_items = get_cart_items_count(request.user)

    # paginating works and if, else part is for the filter
    page_number = request.GET.get("page", 1)
    works = age_restriction_utils.get_safe_works(request)

    if pk == 4:
        genres, authors, flows, regions = Works.objects.main_filter(1)
        works = works.filter(for_interier=True)
        applied_art = age_restriction_utils.get_safe_works(request, applied_art=True).filter(for_interier=True)
        works = list(chain(works, applied_art))

    elif pk:
        genres, authors, flows, regions = Works.objects.main_filter(pk)
        works = works.filter(section_id=pk).order_by("-pub_date")

    if request.GET.get("authors"):
        _id = request.GET["authors"]
        works = age_restriction_utils.get_safe_works(request, obj=works)
        works = works.filter(author__id=_id).order_by("-pub_date")

    if request.GET.get("genres"):
        _id = request.GET["genres"]
        works = age_restriction_utils.get_safe_works(request, obj=works)
        works = works.filter(genre__id=_id).order_by("-pub_date")

    if request.GET.get("regions"):
        _id = request.GET["regions"]
        works = age_restriction_utils.get_safe_works(request, obj=works)
        works = works.filter(regions__id=_id).order_by("-pub_date")

    if request.GET.get("types"):
        _id = request.GET["types"]
        works = age_restriction_utils.get_safe_works(request, obj=works)
        works = works.filter(type__id=_id).order_by("-pub_date")

    if request.GET.get("flows"):
        _id = request.GET["flows"]
        works = age_restriction_utils.get_safe_works(request, obj=works)
        works = works.filter(flow__id=_id).order_by("-pub_date")

    paginator = Paginator(works, 6)
    page_obj = paginator.get_page(page_number)

    # changing data, so we are able to send it as JSON
    regions_dict = {"name": [region.name for region in regions], "id": [region.id for region in regions]}

    # TODO: needs an optimization. Make a new util function
    if get_language() == "en":
        types_dict = [
            {'id': _type.id,
             'name': _type.name_en if _type.name_en else _type.name}
            for _type in types
        ]
        genres_dict = [
            {'id': genre.id,
             'name': genre.name_en if genre.name_en else genre.name}
            for genre in genres
        ]
        authors_dict = [
            {'id': author.id,
             'name': author.name_en if author.name_en else author.name}
            for author in authors
        ]
        sections_dict = [
            {'id': section.id,
             'name': section.name_en if section.name_en else section.name,
             'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'url-api': f"{request.get_host()}{reverse('home_page')}gallery-api/{section.id}",
             }
            for section in sections
        ]
        flows_dict = [
            {'id': flow.id,
             'name': flow.name_en if flow.name_en else flow.name}
            for flow in flows
        ]

        data_dict = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'name': kw.name_en if kw.name_en else kw.name,
             'status': kw.status_en if kw.status_en else kw.status,
             'author': kw.author.name_en if kw.author.name_en else kw.author.name,
             'country': kw.country.name_en if kw.country.name_en else kw.country.name}
            for kw in page_obj.object_list
        ]
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_en if about.title_en else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': 'Our Team'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': 'Experts'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_en if service.name_en else service.name}
            for service in services
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_en if craftsmanship.name_en else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]

    elif get_language() == "uz":
        types_dict = [
            {'id': _type.id,
             'name': _type.name_uz if _type.name_uz else _type.name}
            for _type in types
        ]
        genres_dict = [
            {'id': genre.id,
             'name': genre.name_uz if genre.name_uz else genre.name}
            for genre in genres
        ]
        authors_dict = [
            {'id': author.id,
             'name': author.name_uz if author.name_uz else author.name}
            for author in authors
        ]
        sections_dict = [
            {'id': section.id,
             'name': section.name_uz if section.name_uz else section.name,
             'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'url-api': f"{request.get_host()}{reverse('home_page')}gallery-api/{section.id}",
             }
            for section in sections
        ]
        flows_dict = [
            {'id': flow.id,
             'name': flow.name_uz if flow.name_uz else flow.name}
            for flow in flows
        ]

        data_dict = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'name': kw.name_uz if kw.name_uz else kw.name,
             'status': kw.status_uz if kw.status_uz else kw.status,
             'author': kw.author.name_uz if kw.author.name_uz else kw.author.name,
             'country': kw.country.name_uz if kw.country.name_uz else kw.country.name}
            for kw in page_obj.object_list
        ]
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_uz if about.title_uz else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': 'Bizning Jamoa'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': 'Ekspertlar'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_uz if service.name_uz else service.name}
            for service in services
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_uz if craftsmanship.name_uz else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]

    elif get_language() == "zh_cn":
        types_dict = [
            {'id': _type.id,
             'name': _type.name_zh_cn if _type.name_zh_cn else _type.name}
            for _type in types
        ]
        genres_dict = [
            {'id': genre.id,
             'name': genre.name_zh_cn if genre.name_zh_cn else genre.name}
            for genre in genres
        ]
        authors_dict = [
            {'id': author.id,
             'name': author.name_zh_cn if author.name_zh_cn else author.name}
            for author in authors
        ]
        sections_dict = [
            {'id': section.id,
             'name': section.name_zh_cn if section.name_zh_cn else section.name,
             'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'url-api': f"{request.get_host()}{reverse('home_page')}gallery-api/{section.id}",
             }
            for section in sections
        ]
        flows_dict = [
            {'id': flow.id,
             'name': flow.name_zh_cn if flow.name_zh_cn else flow.name}
            for flow in flows
        ]

        data_dict = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'name': kw.name_zh_cn if kw.name_zh_cn else kw.name,
             'status': kw.status_zh_cn if kw.status_zh_cn else kw.status,
             'author': kw.author.name_zh_cn if kw.author.name_zh_cn else kw.author.name,
             'country': kw.country.name_zh_cn if kw.country.name_zh_cn else kw.country.name}
            for kw in page_obj.object_list
        ]
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_zh_cn if about.title_zh_cn else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': '我們的隊伍'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': '專家'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_zh_cn if service.name_zh_cn else service.name}
            for service in services
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_zh_cn if craftsmanship.name_zh_cn else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]

    else:
        types_dict = [
            {'id': _type.id,
             'name': _type.name_ru if _type.name_ru else _type.name}
            for _type in types
        ]
        genres_dict = [
            {'id': genre.id,
             'name': genre.name_ru if genre.name_ru else genre.name}
            for genre in genres
        ]
        authors_dict = [
            {'id': author.id,
             'name': author.name_ru if author.name_ru else author.name}
            for author in authors
        ]
        sections_dict = [
            {'id': section.id,
             'name': section.name_ru if section.name_ru else section.name,
             'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'url-api': f"{request.get_host()}{reverse('home_page')}gallery-api/{section.id}",
             }
            for section in sections
        ]
        flows_dict = [
            {'id': flow.id,
             'name': flow.name_ru if flow.name_ru else flow.name}
            for flow in flows
        ]

        data_dict = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'name': kw.name_ru if kw.name_ru else kw.name,
             'status': kw.status_ru if kw.status_ru else kw.status,
             'author': kw.author.name_ru if kw.author.name_ru else kw.author.name,
             'country': kw.country.name_ru if kw.country.name_ru else kw.country.name}
            for kw in page_obj.object_list
        ]
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_ru if about.title_ru else about.title}
            for about in abouts]
        our_team = {
            'url': f"{request.get_host()}{reverse('home_page')}about/team",
            'name': 'Наша команда'}
        experts = {
            'url': f"{request.get_host()}{reverse('home_page')}about/experts",
            'name': 'Эксперты'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_ru if service.name_ru else service.name}
            for service in services
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_ru if craftsmanship.name_ru else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]

    abouts.append(experts)
    abouts.append(our_team)

    # context data for sending
    context = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "cart_items": cart_items,
        "sections": sections_dict,
        "authors": authors_dict,
        "regions": regions_dict,
        "lang": get_language(),
        "genres": genres_dict,
        "flows": flows_dict,
        "types": types_dict,
        "data": data_dict,

        'craftsmanships': craftsmanships,
        'country_name': country_name,
        'services': services,
        'abouts': abouts
    }
    return JsonResponse(context)


@login_required()
def profile(request):
    common_context = get_common_context(request)
    auth_user = AuthUsers.objects.get(email__exact=request.user.email)

    template_name = "pages/profile.html"
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your profile has been saved successfully!"))
        else:
            messages.error(request, _("Error in your profile"))

    else:
        form = UpdateProfileForm(instance=request.user)

    context = {
        **common_context,
        'auth_user': auth_user,
        'form': form
    }
    return render(request, template_name, context)


class Abouts(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self):
        common_context = get_common_context(self.request)
        context = {
            **common_context
        }
        return context


class AboutDetail(TemplateView):
    template_name = "pages/about-detail.html"

    def get_context_data(self, id=None):
        about_detail = About.objects.get(id=id)
        common_context = get_common_context(self.request)
        context = {
            **common_context,
            "about_detail": about_detail
        }

        return context


class Artists(TemplateView):
    template_name = "pages/artists.html"

    def get_context_data(self, **kwargs):
        artists = Authors.objects.all()
        countries = Country.objects.all()
        categories = Categories.objects.all()

        common_context = get_common_context(self.request)

        context = {
            **common_context,
            "categories": categories,
            "countries": countries,
            "artists": artists
        }

        return context


class CraftmanshipView(TemplateView):
    template_name = "pages/craftmanship.html"

    def get_context_data(self, slug=None, **kwargs):
        artists = Authors.objects.filter(craftmanship__slug=slug)
        categories = Categories.objects.all()

        common_context = get_common_context(self.request)

        context = {
            **common_context,
            "categories": categories,
            "artists": artists
        }

        return context


class ArtistDetail(TemplateView):
    template_name = "pages/artists-detail.html"

    def get_context_data(self, id=None, **kwargs):
        artist = Authors.objects.get(id=id)
        artists = Authors.objects.all().exclude(id=id)
        works = age_restriction_utils.get_safe_works(self.request).filter(author__id=artist.id)
        applied_arts = age_restriction_utils.get_safe_works(self.request, applied_art=True).filter(author__id=artist.id)

        common_context = get_common_context(self.request)
        context = {
            **common_context,
            "applied_arts": applied_arts,
            "artists": artists,
            "artist": artist,
            "works": works
        }
        return context


class ServicesView(TemplateView):
    template_name = "pages/services.html"

    def get_context_data(self):
        common_context = get_common_context(self.request)
        context = {
            **common_context
        }
        return context


class ServicesDetail(TemplateView):
    template_name = "pages/service-detail.html"

    def get_context_data(self, slug=None, **kwargs):
        service = Services.objects.get(slug=slug)
        slider_images = ServicesImage.objects.filter(service__slug=slug)

        common_context = get_common_context(self.request)
        context = {
            **common_context,
            "slider_images": slider_images,
            "service": service,
        }
        return context


class PublishHouse(TemplateView):
    template_name = "pages/publishing_house.html"

    def get_context_data(self, **kwargs):
        pub_house = get_object_or_404(PublishHouseArt)
        pub_house_images = PublishHouseWork.objects.order_by('-pk')

        common_context = get_common_context(self.request)
        context = {
            **common_context,
            "pub_house": pub_house,
            "pub_house_images": pub_house_images,
        }
        return context


def contact_page(request):
    common_context = get_common_context(request)
    context = {
        **common_context
    }

    return render(request, "pages/contact.html", context)


@login_required()
def cart_page(request):
    cart_total = 0
    products_number = 0
    currency = False
    items_prices = {}

    items = CartItem.objects.filter(cart__user__email=request.user.email, status=CartItemChoices.CART_CART)
    for item in items:
        if item.is_applied_art:
            if item.applied_art.price:
                currency, item.applied_art.price = currency_change_utils.user_currency(request, price=item.applied_art.price)
                cart_total += item.applied_art.price
                items_prices[item.applied_art.name] = item.applied_art.price
                products_number += 1
        else:
            if item.art_work.price:
                currency, item.art_work.price = currency_change_utils.user_currency(request, price=item.art_work.price)
                cart_total += item.art_work.price
                items_prices[item.art_work.name] = item.art_work.price
                products_number += 1

    form = UpdateCheckoutProfileForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateCheckoutProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your profile has been saved successfully!"))
            return redirect('general:order_page')

    common_context = get_common_context(request)
    context = {
        **common_context,
        'products_number': products_number,
        "cart_items": products_number,
        'items_prices': items_prices,
        "cart_total": cart_total,
        "items_in_cart": items,
        'currency': currency,
        'form': form
    }
    return render(request, "pages/basket.html", context)


@login_required()
def order_page(request):
    template_name = "pages/order.html"

    cart = Cart.objects.get(user__email=request.user.email)
    current_user = AuthUsers.objects.get(email=request.user.email)
    cart_items = cart.cart_items.filter(status=CartItemChoices.CART_CART)

    total = 0
    currency = False
    artwork_count = 0
    items_prices = {}

    for item in cart_items:
        if item.is_applied_art:
            if item.applied_art.status == StatusChoices.SOLD:
                messages.error(request, f"Ошибка! Уже продан. Убрано из корзины")
                cart_items.remove(item)
            if item.applied_art.price:
                currency, item.applied_art.price = currency_change_utils.user_currency(request, price=item.applied_art.price)
                total += item.applied_art.price
                items_prices[item.applied_art.name] = item.applied_art.price
                artwork_count += 1
        else:
            if item.art_work.status == StatusChoices.SOLD:
                messages.error(request, f"Ошибка! Уже продан. Убрано из корзины")
                cart_items.remove(item)
            if item.art_work.price:
                currency, item.art_work.price = currency_change_utils.user_currency(request, price=item.art_work.price)
                total += item.art_work.price
                items_prices[item.art_work.name] = item.art_work.price
                artwork_count += 1

    common_context = get_common_context(request)
    context = {
        **common_context,
        'artwork_count': artwork_count,
        'auth_user': current_user,
        'cart_items': artwork_count,
        'currency': currency,
        'total': total
    }
    return render(request, template_name, context)


@login_required()
def favorites_page(request):
    items = CartItem.objects.filter(
        cart__user__email__exact=request.user.email, status=CartItemChoices.CART_WISHLIST
    )
    currency = False
    items_prices = {}
    wishlist_total = 0

    for item in items:
        if item.is_applied_art:
            currency, item.applied_art.price = currency_change_utils.user_currency(request, price=item.applied_art.price)
            wishlist_total += item.applied_art.price
            items_prices[item.applied_art.name] = item.applied_art.price

        else:
            currency, item.art_work.price = currency_change_utils.user_currency(request, price=item.art_work.price)
            wishlist_total += item.art_work.price
            items_prices[item.art_work.name] = item.art_work.price

    common_context = get_common_context(request)
    context = {
        **common_context,
        "wishlist_total": wishlist_total,
        "wishlist_items": items,
        "currency": currency
    }
    return render(request, "pages/favorite.html", context)


@login_required()
def history_page(request):
    order_query = Q(user__email=request.user.email) & ~Q(status='pending')
    orders = Order.objects.filter(order_query).distinct()
    user = AuthUsers.objects.get(email=request.user.email)

    try:
        user = AuthUsers.objects.get(email__exact=request.user.email)
    except AuthUsers.DoesNotExist:
        print("User doesn't exist")

    common_context = get_common_context(request)
    context = {
        "customer": user,
        "orders": orders,
        **common_context
    }
    return render(request, "pages/history.html", context)


def search(request):
    template_name = "pages/catalog.html"
    return render(request, template_name)


def search_api(request):
    context = {}
    abouts = About.objects.all()
    services = Services.objects.all()
    sections = Sections.objects.all()
    all_authors = Authors.objects.all()
    all_countries = Country.objects.all()
    craftsmanships = Craftmanship.objects.all()

    ip = get_ip(request=request)
    country_code, country_name = client_country(ip)

    works = age_restriction_utils.get_safe_works(request)
    applied_art = age_restriction_utils.get_safe_works(request, applied_art=True)

    works = list(works) + list(applied_art)

    if get_language() == "en":
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_en if about.title_en else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': 'Our Team'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': 'Experts'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_en if service.name_en else service.name}
            for service in services
        ]
        sections = [
            {'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'name': section.name_en if section.name_en else section.name}
            for section in sections
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_en if craftsmanship.name_en else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]
        all_authors = [{'id': author.id, 'name': author.name_en if author.name_en else author.name}
                       for author in all_authors]
        all_countries = [{'id': country.id, 'name': country.name_en if country.name_en else country.name}
                         for country in all_countries]

    elif get_language() == "uz":
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_uz if about.title_uz else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': 'Bizning Jamoa'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': 'Ekspertlar'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_uz if service.name_uz else service.name}
            for service in services
        ]
        sections = [
            {'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'name': section.name_uz if section.name_uz else section.name}
            for section in sections
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_uz if craftsmanship.name_uz else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]
        all_authors = [{'id': author.id, 'name': author.name_uz if author.name_uz else author.name}
                       for author in all_authors]
        all_countries = [{'id': country.id, 'name': country.name_uz if country.name_uz else country.name}
                         for country in all_countries]

    elif get_language() == "zh_cn":
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_zh_cn if about.title_zh_cn else about.title}
            for about in abouts]
        our_team = {'url': f"{request.get_host()}{reverse('home_page')}about/team", 'name': '我們的隊伍'}
        experts = {'url': f"{request.get_host()}{reverse('home_page')}about/experts", 'name': '專家'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_zh_cn if service.name_zh_cn else service.name}
            for service in services
        ]
        sections = [
            {'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'name': section.name_zh_cn if section.name_zh_cn else section.name}
            for section in sections
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_zh_cn if craftsmanship.name_zh_cn else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]
        all_authors = [{'id': author.id, 'name': author.name_zh_cn if author.name_zh_cn else author.name}
                       for author in all_authors]
        all_countries = [{'id': country.id, 'name': country.name_zh_cn if country.name_zh_cn else country.name}
                         for country in all_countries]

    else:
        abouts = [
            {'url': f"{request.get_host()}{reverse('home_page')}about/{about.id}",
             'name': about.title_ru if about.title_ru else about.title}
            for about in abouts]
        our_team = {
            'url': f"{request.get_host()}{reverse('home_page')}about/team",
            'name': 'Наша команда'}
        experts = {
            'url': f"{request.get_host()}{reverse('home_page')}about/experts",
            'name': 'Эксперты'}
        services = [
            {'url': f"{request.get_host()}{reverse('home_page')}services/{service.slug}",
             'name': service.name_ru if service.name_ru else service.name}
            for service in services
        ]
        sections = [
            {'url': f"{request.get_host()}{reverse('home_page')}gallery/{section.id}",
             'name': section.name_ru if section.name_ru else section.name}
            for section in sections
        ]
        craftsmanships = [
            {'url': f"{request.get_host()}{reverse('home_page')}artists/craftmanship/{craftsmanship.slug}",
             'name': craftsmanship.name_ru if craftsmanship.name_ru else craftsmanship.name}
            for craftsmanship in craftsmanships
        ]
        all_authors = [{'id': author.id, 'name': author.name_ru if author.name_ru else author.name}
                       for author in all_authors]
        all_countries = [{'id': country.id, 'name': country.name_ru if country.name_ru else country.name}
                         for country in all_countries]

    abouts.append(experts)
    abouts.append(our_team)

    page_number = request.GET.get("page", 1)
    paginator = Paginator(works, 6)
    page_obj = paginator.get_page(page_number)
    context['page'] = {
        "current": page_obj.number,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
    }

    if get_language() == "en":
        works_result = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'size': kw.size,
             'name': kw.name_en if kw.name_en else kw.name,
             'status': kw.status_en if kw.status_en else kw.status,
             'material': kw.material_en if kw.material_en else kw.material,
             'author': kw.author.name_en if kw.author.name_en else kw.author.name,
             'country': kw.country.name_en if kw.country.name_en else kw.country.name,
             }
            for kw in page_obj.object_list
        ]

    elif get_language() == "uz":
        works_result = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'size': kw.size,
             'name': kw.name_uz if kw.name_uz else kw.name,
             'status': kw.status_uz if kw.status_uz else kw.status,
             'material': kw.material_uz if kw.material_uz else kw.material,
             'author': kw.author.name_uz if kw.author.name_uz else kw.author.name,
             'country': kw.country.name_uz if kw.country.name_uz else kw.country.name}
            for kw in page_obj.object_list
        ]

    elif get_language() == "ru":
        works_result = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'size': kw.size,
             'name': kw.name_ru if kw.name_ru else kw.name,
             'status': kw.status_ru if kw.status_ru else kw.status,
             'material': kw.material_ru if kw.material_ru else kw.material,
             'author': kw.author.name_ru if kw.author.name_ru else kw.author.name,
             'country': kw.country.name_ru if kw.country.name_ru else kw.country.name}
            for kw in page_obj.object_list
        ]
    elif get_language() == "zh_cn":
        works_result = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'size': kw.size,
             'name': kw.name_zh_cn if kw.name_zh_cn else kw.name,
             'status': kw.status_zh_cn if kw.status_zh_cn else kw.status,
             'material': kw.material_zh_cn if kw.material_zh_cn else kw.material,
             'author': kw.author.name_zh_cn if kw.author.name_zh_cn else kw.author.name,
             'country': kw.country.name_zh_cn if kw.country.name_zh_cn else kw.country.name}
            for kw in page_obj.object_list
        ]
    else:
        works_result = [
            {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
             'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
             'size': kw.size,
             'name': kw.name_ru if kw.name_ru else kw.name,
             'status': kw.status_ru if kw.status_ru else kw.status,
             'material': kw.material_ru if kw.material_ru else kw.material,
             'author': kw.author.name_ru if kw.author.name_ru else kw.author.name,
             'country': kw.country.name_ru if kw.country.name_ru else kw.country.name}
            for kw in page_obj.object_list
        ]

    context['craftsmanships'] = craftsmanships
    context['all_countries'] = all_countries
    context['works_result'] = works_result
    context['all_authors'] = all_authors
    context['sections'] = sections
    context['services'] = services
    context['abouts'] = abouts

    if request.GET.get("search"):
        key = request.GET.get("search")
        if len(key) > 3:
            requirement = True
            if Works.objects.filter(name__icontains=key).exists() or \
                     AppliedArt.objects.filter(name__icontains=key).exists():

                if Works.objects.filter(name__icontains=key).exists():
                    works_result = Works.objects.filter(name__icontains=key)
                else:
                    works_result = AppliedArt.objects.filter(name__icontains=key)

                page_number = request.GET.get("page", 1)
                paginator = Paginator(works_result, 6)
                page_obj = paginator.get_page(page_number)
                context['page'] = {
                    "current": page_obj.number,
                    "has_next": page_obj.has_next(),
                    "has_previous": page_obj.has_previous(),
                }

                if get_language() == "en":
                    works_result = [
                        {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
                         'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
                         'size': kw.size,
                         'name': kw.name_en if kw.name_en else kw.name,
                         'status': kw.status_en if kw.status_en else kw.status,
                         'material': kw.material_en if kw.material_en else kw.material,
                         'author': kw.author.name_en if kw.author.name_en else kw.author.name,
                         'country': kw.country.name_en if kw.country.name_en else kw.country.name,
                         }
                        for kw in page_obj.object_list
                    ]

                elif get_language() == "uz":
                    works_result = [
                        {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
                         'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
                         'size': kw.size,
                         'name': kw.name_uz if kw.name_uz else kw.name,
                         'status': kw.status_uz if kw.status_uz else kw.status,
                         'material': kw.material_uz if kw.material_uz else kw.material,
                         'author': kw.author.name_uz if kw.author.name_uz else kw.author.name,
                         'country': kw.country.name_uz if kw.country.name_uz else kw.country.name}
                        for kw in page_obj.object_list
                    ]

                elif get_language() == "ru":
                    works_result = [
                        {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
                         'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
                         'size': kw.size,
                         'name': kw.name_ru if kw.name_ru else kw.name,
                         'status': kw.status_ru if kw.status_ru else kw.status,
                         'material': kw.material_ru if kw.material_ru else kw.material,
                         'author': kw.author.name_ru if kw.author.name_ru else kw.author.name,
                         'country': kw.country.name_ru if kw.country.name_ru else kw.country.name}
                        for kw in page_obj.object_list
                    ]
                elif get_language() == "zh_cn":
                    works_result = [
                        {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
                         'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
                         'size': kw.size,
                         'name': kw.name_zh_cn if kw.name_zh_cn else kw.name,
                         'status': kw.status_zh_cn if kw.status_zh_cn else kw.status,
                         'material': kw.material_zh_cn if kw.material_zh_cn else kw.material,
                         'author': kw.author.name_zh_cn if kw.author.name_zh_cn else kw.author.name,
                         'country': kw.country.name_zh_cn if kw.country.name_zh_cn else kw.country.name}
                        for kw in page_obj.object_list
                    ]
                else:
                    works_result = [
                        {'photo': kw.photo.url, 'period': kw.year_of_creation, 'lot': kw.u_id,
                         'url': f"{request.get_host()}{reverse('home_page')}catalog/{kw.slug}",
                         'size': kw.size,
                         'name': kw.name_ru if kw.name_ru else kw.name,
                         'status': kw.status_ru if kw.status_ru else kw.status,
                         'material': kw.material_ru if kw.material_ru else kw.material,
                         'author': kw.author.name_ru if kw.author.name_ru else kw.author.name,
                         'country': kw.country.name_ru if kw.country.name_ru else kw.country.name}
                        for kw in page_obj.object_list
                    ]

            else:
                works_result = []

            if Authors.objects.filter(name__icontains=key).exists():
                authors_result = Authors.objects.filter(name__icontains=key)

                if get_language() == "en":
                    authors_result = [
                        {'id': author.id,
                         'thumbnail': author.thumbnail.url,
                         'name': author.name_en if author.name_en else author.name,
                         'url': f"{request.get_host()}{reverse('home_page')}artist/{author.id}"}
                        for author in authors_result
                    ]

                elif get_language() == "uz":
                    authors_result = [
                        {'id': author.id,
                         'thumbnail': author.thumbnail.url,
                         'name': author.name_uz if author.name_uz else author.name,
                         'url': f"{request.get_host()}{reverse('home_page')}artist/{author.id}"}
                        for author in authors_result
                    ]

                elif get_language() == "ru":
                    authors_result = [
                        {'id': author.id,
                         'thumbnail': author.thumbnail.url,
                         'name': author.name_ru if author.name_ru else author.name,
                         'url': f"{request.get_host()}{reverse('home_page')}artist/{author.id}"}
                        for author in authors_result
                    ]

                elif get_language() == "zh_cn":
                    authors_result = [
                        {'id': author.id,
                         'thumbnail': author.thumbnail.url,
                         'name': author.name_zh_cn if author.name_zh_cn else author.name,
                         'url': f"{request.get_host()}{reverse('home_page')}artist/{author.id}"}
                        for author in authors_result
                    ]

                else:
                    authors_result = [
                        {'id': author.id,
                         'thumbnail': author.thumbnail.url,
                         'name': author.name_ru if author.name_ru else author.name,
                         'url': f"{request.get_host()}{reverse('home_page')}artist/{author.id}"}
                        for author in authors_result
                    ]

            else:
                authors_result = []

        else:
            authors_result = []
            works_result = []
            requirement = False

        context['authors_result'] = authors_result
        context['country_name'] = country_name
        context['works_result'] = works_result
        context['requirement'] = requirement
    return JsonResponse(context)


def works_filter(request):
    template = "pages/filter.html"
    works = age_restriction_utils.get_safe_works(request)
    local_filter = filters.WorkFilter(request.GET, queryset=works)
    works = local_filter.qs

    context = {'works': works}
    return render(request, template, context)


def sell(request):
    template_name = 'pages/sell.html'

    if request.POST:
        try:
            view = request.FILES['view']
            size = request.POST.get("size")
            name = request.POST.get("name")
            date = request.POST.get("date")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            price = request.POST.get("price")
            genre = request.POST.get("genre")
            style = request.POST.get("style")
            seller = request.POST.get("seller")
            author = request.POST.get("author")
            period = request.POST.get("period")
            design = request.POST.get("design")
            section = request.POST.get("section")
            currency = request.POST.get("currency")
            materials = request.POST.get("materials")
            condition = request.POST.get("condition")

            Sell.objects.create(
                section=section,
                view=view,
                genre=genre,
                style=style,
                author=author,
                name=name,
                date=date,
                period=period,
                materials=materials,
                size=size,
                design=design,
                condition=condition,
                price=price,
                currency=currency,
                seller=seller,
                phone=phone,
                email=email
            )
            messages.success(request, 'Запрос успешно отправлен')

            return redirect("home_page")

        except Exception as e:
            print(e)
            messages.error(
                request, 'An error has occurred during registration')

    common_context = get_common_context(request)

    context = {
        **common_context
    }

    return render(request, template_name, context)


class TeamView(TemplateView):
    template_name = "pages/team.html"

    def get_context_data(self):
        group = TeamMember.objects.all()
        team = []

        for member in group:
            if not member.is_expert:
                team.append(member)

        common_context = get_common_context(self.request)
        context = {
            "team": team,
            **common_context
        }
        return context


class ExpertsView(TemplateView):
    template_name = "pages/team.html"

    def get_context_data(self):
        experts = ExpertMember.objects.all().order_by('order_number')

        common_context = get_common_context(self.request)
        context = {
            "member": experts,
            **common_context
        }
        return context


class GenresView(TemplateView):
    template_name = "pages/genres.html"

    def get_context_data(self):
        common_context = get_common_context(self.request)
        genres = Categories.objects.all()

        context = {
            "genres": genres,
            **common_context
        }
        return context


class GenresDetailView(DetailView):
    template_name = "pages/genres-detail.html"
    model = Categories

    def get_context_data(self, **kwargs):
        common_context = get_common_context(self.request)
        obj = super().get_object()
        works = age_restriction_utils.get_safe_works(self.request).filter(genre__slug=obj.slug).order_by('-pub_date')
        if works.count() >= 12:
            rand_works = random.sample(list(works), 12)
        elif works.count() in range(7, 12):
            rand_works = random.sample(list(works), 7)
        else:
            rand_works = []

        context = {
            **common_context,
            "works": rand_works
        }
        return context


class AppliedArtTypesView(TemplateView):
    template_name = "pages/appliedart-types.html"

    def get_context_data(self):
        common_context = get_common_context(self.request)
        genres = WorkType.objects.all()

        context = {
            "genres": genres,
            **common_context
        }
        return context


class TeamMemberExtraView(TemplateView):
    template_name = 'pages/team.html'

    def get_context_data(self):
        common_context = get_common_context(self.request)
        team_member_extra = TeamMemberExtra.objects.all().order_by('order_number')

        context = {
            'member': team_member_extra,
            **common_context
        }
        return context


class PartnersView(TemplateView):
    template_name = 'pages/partner.html'

    def get_context_data(self):
        common_context = get_common_context(self.request)
        partners = Partner.objects.all()

        context = {
            'partners': partners,
            **common_context
        }
        return context


class AacView(TemplateView):
    template_name = 'pages/aac.html'

    def get_context_data(self):
        common_context = get_common_context(self.request)
        aac = Aac.objects.all()
        aac_member = AacMember.objects.all().order_by('order_number')

        context = {
            'aac': aac,
            'aac_member': aac_member,
            **common_context
        }
        return context


class AocvView(TemplateView):
    template_name = 'pages/aocv.html'

    def get_context_data(self):
        common_context = get_common_context(self.request)
        aocv = Aocv.objects.all()
        aocv_member = AocvMember.objects.all().order_by('order_number')

        context = {
            'aocv': aocv,
            'aocv_member': aocv_member,
            **common_context
        }
        return context


class AuctionRulesView(TemplateView):
    template_name = 'pages/auctionrules.html'

    def get_context_data(self):
        common_context = get_common_context(self.request)
        auctionrules = AuctionRules.objects.all()

        context = {
            'auctionrules': auctionrules,
            **common_context
        }
        return context


class AuctionView(TemplateView):
    template_name = 'pages/auctions.html'

    def get_context_data(self):
        common_context = get_common_context(self.request)
        auction = Auction.objects.all()
        date_now = datetime.datetime.now()

        context = {
            'auction': auction,
            'date_now': date_now,
            **common_context
        }
        return context


class AuctionDetail(TemplateView):
    template_name = 'pages/auction-detail.html'

    def get_context_data(self, slug=None, **kwargs):
        auction = get_object_or_404(Auction, slug=slug)
        lots = Lots.objects.filter(auction=auction).order_by('number_lot')
        common_context = get_common_context(self.request)

        context = {
            'auction': auction,
            'lots': lots,
            **common_context
        }

        return context


def appliedart_types_detail(request, num):
    template_name = "pages/appliedart-types-detail.html"
    common_context = get_common_context(request)
    rand_works = []
    if age_restriction_utils.get_safe_works(request, applied_art=True).filter(vid__id=num).exists():
        works = age_restriction_utils.get_safe_works(request, applied_art=True).filter(vid__id=num).order_by('-pub_date')

        if works.count() >= 12:
            rand_works = random.sample(list(works), 12)
        elif works.count() in range(7, 12):
            rand_works = random.sample(list(works), 7)

    context = {
        **common_context,
        "works": rand_works
    }
    return render(request, template_name, context)


def robot(request):
    context = {
        'Host': 'https://artv.l-b.uz/',
        'User-Agent': '*',
        'Allow': '/'
    }
    return JsonResponse(context)

