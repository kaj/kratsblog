from django.contrib import admin
from blog.models import *
from image.models import Image

class ImagesInline(admin.TabularInline):
    model = Image
    extra = 3
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ImagesInline, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name == 'caption':
            field.widget.attrs['rows'] = 3
        return field

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'posted_time', 'created_at', 'updated_at',
        'first_image'
    )
    search_fields = ('title', 'content')
    ordering = ('-updated_at', )
    date_hierarchy = 'posted_time'
    exclude = ('slug',)
    # Good stuff, but may need more horizontal screen space than its worth.
    # list_filter = ('posted_time', 'updated_at', 'created_at')
    inlines = (ImagesInline,)

admin.site.register(Post, PostAdmin)
