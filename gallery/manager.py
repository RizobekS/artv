import random
from datetime import datetime
from django.db import models
from django.db.models import Q

from accounts.models import Authors
from general.models import Flow, Categorization


class WorksManager(models.Manager):

    def random_filter(self):
        works = self.all().order_by('-pub_date')
        if works.count() >= 12:
            rand_works = random.sample(list(works), 12)
        elif works.count() in range(7, 12):
            rand_works = random.sample(list(works), 7)
        else:
            rand_works = []
        return rand_works

    def main_filter(self, section_id):
        categories = Categorization.objects.filter(section__id=section_id)
        authors = Authors.objects.filter(occupation1__in=categories)
        flows = Flow.objects.filter(category__in=categories)
        works = self.filter(section=section_id)
        genres = []
        regions = []
        for work in works:
            for region in work.regions.all():
                regions.append(region)
            for genre in work.genre.all():
                genres.append(genre)

        return set(genres), set(authors), set(flows), set(regions)

    def filter_by_author(self, author_id):
        works = self.objects.filter(author=author_id)
        return works

    def filter_by_type(self, type_of_work):
        works = self.filter(type__id=type_of_work.id)
        return works

    def filter_by_date(self, slug):
        if slug == "all":
            works = self.all()
        elif slug == "today":
            today = datetime.today().date()
            works = self.filter(pub_date__date=today)
        elif slug == "month":
            month = datetime.today().date().month
            works = self.filter(pub_date__date__month=month)
        else:
            works = self.filter(pub_date__date__month=slug)
        return works

    def filter_by_events(self, slug):

        def get_id(slug):
            id = slug.split("-")[1]
            return id

        if "clear" in slug:
            works = self.all()

        if "author" in slug:
            id = get_id(slug)
            works = self.filter(author__id=id)
        elif "genre" in slug:
            id = get_id(slug)
            works = self.filter(genre__id=id)
        elif "region" in slug:
            id = get_id(slug)
            works = self.filter(regions__id__contains=id)
        elif "type" in slug:
            id = get_id(slug)
            works = self.filter(type__id=id)
        elif "flow" in slug:
            id = get_id(slug)
            works = self.filter(flow__id=id)

        return works.order_by("-pub_date")

    def search_items(self, key):
        authors = Authors.objects.filter(
            name__contains=key).values_list("id", flat=True)
        if authors:
            q = Q(author__id__in=list(authors))
        else:
            q = Q(name__contains=key) | Q(
                description__contains=key)

        works = self.filter(q)
        return works
