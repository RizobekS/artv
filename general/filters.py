import django_filters
from gallery.models import Works


class WorkFilter(django_filters.FilterSet):
    class Meta:
        model = Works
        fields = ['country', 'genre']
