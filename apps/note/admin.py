from django.contrib import admin

from apps.note.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = 'id', 'author', 'title', 'is_public', 'created_at', 'updated_at'
    list_filter = 'author', 'is_public'
    search_fields = 'title', 'text'
