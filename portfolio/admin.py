from django import forms
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from models import Tag, Project


class TagAdmin(TranslationAdmin):
    list_display = ('name', 'category')
    prepopulated_fields = {'slug_pl': ('name_pl',), 'slug_en': ('name_en',)}
    #prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    search_fields = ('name',)


class ProjectAdmin(TranslationAdmin):
    fieldsets = [
        (None, {'fields': ['tags', 'name', 'slug', 'description', 'status']}),
        ('Date', {'fields': ['created', 'modified'], 'classes': ['collapse']}),
    ]
    list_display = ('position', 'name', 'status')
    list_display_links = ('name',)
    list_filter = ('tags',)
    search_fields = ('name', 'description')
    list_editable = ['position']
    prepopulated_fields = {'slug_pl': ('name_pl',), 'slug_en': ('name_en',)}
    #prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
