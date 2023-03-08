from django import template

register = template.Library()



@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def get_arr_time(Queryset):
    return Queryset.arr_time

@register.filter
def get_dep_time(Queryset):
    return Queryset.dep_time
@register.filter
def get_arr_station_name(Queryset):
    return Queryset.arr_station_name
@register.filter
def get_dep_station_name(Queryset):
    return Queryset.dep_station_name
@register.filter
def get_arr_date(Queryset):
    return Queryset.arr_date


