import csv
import datetime
from django.core import serializers
from django.http import HttpResponse

from django.contrib import admin
from .models import Post, Comment

# Register your models here.

# ACTIONS
def export_as_json(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename={}.json'.format(opts.verbose_name)
    serializers.serialize("json", queryset, stream=response)
    return response
export_as_json.short_description = 'Export to JSON'

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # write the header row
    writer.writerow([field.verbose_name for field in fields])
    #write data row
    for obj in queryset:
        datarow = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            datarow.append(value)
        writer.writerow(datarow)
    return response
export_to_csv.short_description = 'Export to CSV'

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'activate']
    list_filter = ['status', 'created', 'updated', 'author', 'activate']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author',]
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    actions = [export_to_csv, export_as_json]

admin.site.register(Post, PostAdmin)

admin.site.register(Comment)
