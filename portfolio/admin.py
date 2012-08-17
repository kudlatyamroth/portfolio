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


class MyEditorWidget(forms.Textarea):
    class Media:
        css = { 'all' : ( 'css/ui-lightness/jquery-ui-1.8.23.css', 'js/markitup/skins/markitup/style.css', 'js/markitup/sets/default/style.css', 'css/markitup.css') }
        js = (
            'js/jquery-1.8.0.min.js',
            'js/jquery-ui-1.8.23.min.js',
            'js/markitup/jquery.markitup.js',
            'js/markitup/sets/default/set.js',
            'js/enable_editor.js',
        )

    def __init__(self, attrs={}):
        editorClass = ' myeditor'
        try:
            if editorClass not in attrs['class']:
                attrs['class'] += editorClass
        except KeyError:
            attrs['class'] = editorClass

        super(MyEditorWidget, self).__init__(attrs=attrs)

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


admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
