from django.core.files import File
from django.db.models.fields.files import FileDescriptor, FieldFile, FileField
from django.utils.translation import ugettext_lazy, ugettext as _
from django.utils.safestring import mark_safe
from django.db.models import signals
from my_widgets import forms
import re, os, sys, commands

class VideoOrImageFile(File):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with images and videos.
    """
    def _get_width(self):
        return self._get_videoorimage_dimensions()[0]
    width = property(_get_width)

    def _get_height(self):
        return self._get_videoorimage_dimensions()[1]
    height = property(_get_height)

    def _get_videoorimage_dimensions(self):
        if not hasattr(self, '_dimensions_cache'):
            close = self.closed
            self.open()
            self._dimensions_cache = get_videoorimage_dimensions(self.path, close=close)
#            self._dimensions_cache = get_videoorimage_dimensions(self, close=close)
        return self._dimensions_cache

def get_videoorimage_dimensions(file_or_path, close=False):
    """
    Returns the (width, height) of an image or video, given an open file or a path.  Set
    'close' to True to close the file at the end if it is initially in an open
    state.
    """
    if not forms.is_video(file_or_path):
        # Try to import PIL in either of the two ways it can end up installed.
        try:
            from PIL import ImageFile as PILImageFile
        except ImportError:
            import ImageFile as PILImageFile

        p = PILImageFile.Parser()
        if hasattr(file_or_path, 'read'):
            file = file_or_path
            file_pos = file.tell()
            file.seek(0)
        else:
            file = open(file_or_path, 'rb')
            close = True
        try:
            while 1:
                data = file.read(1024)
                if not data:
                    break
                p.feed(data)
                if p.image:
                    return p.image.size
            return None
        finally:
            if close:
                file.close()
            else:
                file.seek(file_pos)
    else:
        ffmpegdimm = "/home/kudlaty/bin/ffmpeg -i %s" % file_or_path
#        ffmpegdimm = "ffmpeg -i %s" % file_or_path
        pattern = re.compile(r'Stream.*Video.*([0-9]{3,})x([0-9]{3,})')
        try:
            dimm_result = commands.getoutput(ffmpegdimm)
            match = pattern.search(dimm_result)
            if match:
                x, y = map(int, match.groups()[0:2])
            else:
                x = y = 0

            return (x, y)
        except:
            raise Exception("coc poszlo nie tak")
#        finally:
#            raise Exception("to x: %s, a to y: %s, a to result: %s" % (x,y,dimm_result))
#            file_or_path.seek(file_or_path.tell())

class VideoOrImageFileDescriptor(FileDescriptor):
    """
    Just like the FileDescriptor, but for VideoOrImageFields. The only difference is
    assigning the width/height to the width_field/height_field, if appropriate.
    """
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super(VideoOrImageFileDescriptor, self).__set__(instance, value)

        # To prevent recalculating image dimensions when we are instantiating
        # an object from the database (bug #11084), only update dimensions if
        # the field had a value before this assignment.  Since the default
        # value for FileField subclasses is an instance of field.attr_class,
        # previous_file will only be None when we are called from
        # Model.__init__().  The VideoOrImageField.update_dimension_fields method
        # hooked up to the post_init signal handles the Model.__init__() cases.
        # Assignment happening outside of Model.__init__() will trigger the
        # update right here.
        if previous_file is not None:
            self.field.update_dimension_fields(instance, force=True)

class VideoOrImageFieldFile(VideoOrImageFile, FieldFile):
    def delete(self, save=True):
        # Clear the image dimensions cache
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache
        super(VideoOrImageFieldFile, self).delete(save)

class VideoOrImageField(FileField):
    attr_class = VideoOrImageFieldFile
    descriptor_class = VideoOrImageFileDescriptor
    description = ugettext_lazy("File path")

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.width_field, self.height_field = width_field, height_field
        FileField.__init__(self, verbose_name, name, **kwargs)

    def contribute_to_class(self, cls, name):
        super(VideoOrImageField, self).contribute_to_class(cls, name)
        # Attach update_dimension_fields so that dimension fields declared
        # after their corresponding image field don't stay cleared by
        # Model.__init__, see bug #11196.
        signals.post_init.connect(self.update_dimension_fields, sender=cls)

    def update_dimension_fields(self, instance, force=False, *args, **kwargs):
        """
        Updates field's width and height fields, if defined.

        This method is hooked up to model's post_init signal to update
        dimensions after instantiating a model instance.  However, dimensions
        won't be updated if the dimensions fields are already populated.  This
        avoids unnecessary recalculation when loading an object from the
        database.
        Dimensions can be forced to update with force=True, which is how
        VideoOrImageFileDescriptor.__set__ calls this method.
        """
        # Nothing to update if the field doesn't have have dimension fields.
        has_dimension_fields = self.width_field or self.height_field
        if not has_dimension_fields:
            return

        # getattr will call the VideoOrImageFileDescriptor's __get__ method, which
        # coerces the assigned value into an instance of self.attr_class
        # (VideoOrImageFieldFile in this case).
        file = getattr(instance, self.attname)

        # Nothing to update if we have no file and not being forced to update.
        if not file and not force:
            return

        dimension_fields_filled = not(
            (self.width_field and not getattr(instance, self.width_field))
            or (self.height_field and not getattr(instance, self.height_field))
        )
        # When both dimension fields have values, we are most likely loading
        # data from the database or updating an image field that already had
        # an image stored.  In the first case, we don't want to update the
        # dimension fields because we are already getting their values from the
        # database.  In the second case, we do want to update the dimensions
        # fields and will skip this return because force will be True since we
        # were called from VideoOrImageFileDescriptor.__set__.
        if dimension_fields_filled and not force:
            return

        # file should be an instance of VideoOrImageFieldFile or should be None.
        if file:
            width = file.width
            height = file.height
        else:
            # No file, so clear dimensions fields.
            width = None
            height = None

        # Update the width and height fields.
        if self.width_field:
            setattr(instance, self.width_field, width)
        if self.height_field:
            setattr(instance, self.height_field, height)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.VideoOrImageField}
        defaults.update(kwargs)
        return super(VideoOrImageField, self).formfield(**defaults)
