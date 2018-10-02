from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Podcasts


class PodcastsResource(resources.ModelResource):
    class Meta:
        model = Podcasts
        # fields = ('id', 'title',)
        # export_order = ('id', 'title',)

@admin.register(Podcasts)
class PodcastsAdmin(ImportExportModelAdmin):
    resource_class = PodcastsResource

# Register your models here.
# admin.site.register(Podcasts)