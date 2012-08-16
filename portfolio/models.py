import datetime
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    status = models.BooleanField(default=True)
    position = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        model = self.__class__

        if self.position is None:
            try:
                last = model.objects.order_by('-position')[0]
                self.position = last.position + 1
            except IndexError:
                self.position = 0

        return super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-position',]

    #def get_description(self):
        #return mark_safe(render_bbcode(self.description))


#class Gallery(models.Model):
    #project = models.ForeignKey(Project, null=True, blank=True)
    #name = models.CharField(max_length=255, null=True, blank=True)
    #main = models.BooleanField()
    #file = ThumbnailVideoOrImageField(upload_to='files', thumb_aspect=False, null=True, blank=True)
    #status = models.BooleanField(default=True)
    #created = models.DateTimeField(default=datetime.datetime.now)
    #modified = models.DateTimeField(default=datetime.datetime.now)
    #position = models.IntegerField(null=True, blank=True)

    #def file_thumb(self):
        #if self.file:
            #return u'<img src="%s" />' % self.file.thumb_url
        #else:
            #return '(no image)'
    #file_thumb.short_description = 'Thumb'
    #file_thumb.allow_tags = True

    #def save(self, *args, **kwargs):
        #model = self.__class__

        #if self.position is None:
            #try:
                #last = model.objects.filter(project = self.project).order_by('-position')[0]
                #self.position = last.position + 1
            #except IndexError:
                #self.position = 0

        #return super(Gallery, self).save(*args, **kwargs)

    #class Meta:
        #ordering = ['position']
        #verbose_name_plural = "galleries"

    #def __unicode__(self):
        #if self.name:
            #return self.name
        #else:
            #return 'name'
