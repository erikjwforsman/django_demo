import django_filters
from .models import Ohje
from django_filters import NumberFilter, CharFilter


class OhjeFilter(django_filters.FilterSet):
    max_time = NumberFilter(field_name="cooking_time", lookup_expr="lte")
    ing = CharFilter(field_name="ingredients", lookup_expr="icontains")

    class Meta:
        model = Ohje
        fields = ["dish"]

        #Myös näin
        #fields = "__all__"
        #exclude = ["...", "..."]
