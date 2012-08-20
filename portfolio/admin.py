from django import forms
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin
from MyWidgets.widget import MyEditorWidget

from models import Tag, Project, Gallery


class TagAdmin(TranslationAdmin):
    list_display = ('name', 'category')
    prepopulated_fields = {'slug_pl': ('name_pl',), 'slug_en': ('name_en',)}
    #prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    search_fields = ('name',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
            'description': MyEditorWidget,
            'description_en': MyEditorWidget,
            'description_pl': MyEditorWidget,
        }

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

    form = ProjectForm


class GalleryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['project', 'main', 'name', 'file', 'status']}),
        ('Date', {'fields': ['created', 'modified'], 'classes': ['collapse']}),
    ]
    list_display = ('position', 'name', 'status', 'main', 'file')
    list_display_links = ('name','file')
    list_filter = ('status', 'main', 'name',)
    search_fields = ('name',)
    list_editable = ['position']


admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Gallery, GalleryAdmin)
