from django.contrib import admin
from .models import Album, MusicFile

class MusicFileInline(admin.TabularInline):
    model = MusicFile
    extra = 1

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """
    Allows managing Albums and their associated music files in a single page.
    """
    list_display = ('name', 'author')
    inlines = [MusicFileInline]

@admin.register(MusicFile)
class MusicFileAdmin(admin.ModelAdmin):
    """
    Separate admin for MusicFile if needed.
    """
    list_display = ('title', 'album', 'order', 'duration')
    list_filter = ('album',)
