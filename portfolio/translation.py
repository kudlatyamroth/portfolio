from modeltranslation.translator import translator, TranslationOptions

from models import Tag, Project


class TagTrans(TranslationOptions):
    fields = ('name', 'slug',)

class ProjectTrans(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(Tag, TagTrans)
translator.register(Project, ProjectTrans)
