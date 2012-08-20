import re, os, sys, commands

from django.core.files import File
from django.core.files.images import get_image_dimensions
from django.db.models.fields.files import ImageFileDescriptor, ImageFieldFile, ImageField
from django.utils.translation import ugettext_lazy, ugettext as _

import forms


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
        return get_image_dimensions(file_or_path, close)
    else:
        ffmpegdimm = "ffmpeg -i %s" % file_or_path
        pattern = re.compile(r'Stream.*Video.*([0-9]{3,})x([0-9]{3,})')
        try:
            dimm_result = commands.getoutput(ffmpegdimm)
            match = pattern.search(dimm_result)
            if match:
                x, y = map(int, match.groups()[0:2])
            else:
                x = y = 0

            return (x, y)
        finally:
            pass

class VideoOrImageFieldFile(VideoOrImageFile, ImageFieldFile):

    def delete(self, save=True):
        # Clear the image dimensions cache
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache
        super(VideoOrImageFieldFile, self).delete(save)

class VideoOrImageField(ImageField):
    attr_class = VideoOrImageFieldFile
    descriptor_class = ImageFileDescriptor
    description = ugettext_lazy("Video or Image")

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.width_field, self.height_field = width_field, height_field
        super(VideoOrImageField, self).__init__(self, verbose_name, name, width_field, height_field, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.VideoOrImageField}
        defaults.update(kwargs)
        return super(VideoOrImageField, self).formfield(**defaults)
