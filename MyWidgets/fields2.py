from my_widgets.fields import VideoOrImageField, VideoOrImageFieldFile, get_videoorimage_dimensions
from my_widgets.forms import is_video, is_video_buffer
from PIL import Image
import os, sys, commands

def _add_thumb(s):
    parts = s.split(".")
    parts.insert(-1, "thumb")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)

def _add_webm(s):
    parts = s.split(".")
    if parts[-1].lower() not in ['webm', 'webm']:
        parts[-1] = 'webm'
    return ".".join(parts)

def is_webm(s):
    parts = s.split(".")
    if parts[-1].lower() not in ['webm', 'webm']:
        return False
    else:
        return True

class ThumbnailVideoOrImageFieldFile(VideoOrImageFieldFile):
    def _get_thumb_path(self):
        return _add_thumb(self.path)
    thumb_path = property(_get_thumb_path)

    def _get_webm_path(self):
        if(is_video(self.path)):
            return _add_webm(self.path)
        else:
            return ""
    webm_path = property(_get_webm_path)

    def _get_thumb_url(self):
        return _add_thumb(self.url)
    thumb_url = property(_get_thumb_url)

    def _get_webm_url(self):
        if(is_video(self.path)):
            return _add_webm(self.url)
        else:
            return ""
    webm_url = property(_get_webm_url)

    def _get_is_video(self):
        return is_video(self.path)
    vidimg = property(_get_is_video)

#    def _get_videoorimage_dimensions(self):
#        close = self.closed
#        self.open()
#        self._dimensions_cache = get_videoorimage_dimensions(self.path, close=close)
#        return self._dimensions_cache

#    def _get_width(self):
#        return self._get_videoorimage_dimensions()[0]
#    width = property(_get_width)

#    def _get_height(self):
#        return self._get_videoorimage_dimensions()[1]
#    height = property(_get_height)

    def save(self, name, content, save=True):
        super(ThumbnailVideoOrImageFieldFile, self).save(name, content, save)
        file = self.path

        if not is_video(file):
            if self.field.thumb_aspect:
                img = Image.open(self.path)
                img.thumbnail(
                    (self.field.thumb_width, self.field.thumb_height),
                    Image.ANTIALIAS
                )
                img.save(self.thumb_path, 'JPEG')
            else:
                img = Image.open(self.path)
                img = img.resize(
                    (self.field.thumb_width, self.field.thumb_height),
                    Image.ANTIALIAS
                )
                img.save(self.thumb_path, 'JPEG')
        else:
            ffmpeg = "ffmpeg -i %s -vcodec libvpx -level 216 -qmax 42 -qmin 10 -vb 2M -maxrate 24M -minrate 100k -b 3900k -pass 1 -an -f webm -y %s" % (self.path, self.webm_path)
            grabimage = "ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 200x150 %s" % (self.path, self.thumb_path)
            try:
                grab = commands.getoutput(grabimage)
            except:
                raise Exception("FFmpeg polegl na wyciaganiu obrazka")

            if not is_webm(self.path):
                try:
                    ffmpegresult = commands.getoutput(ffmpeg)
                    try:
                        s = os.stat(self.webm_path)
                        fsize = s.st_size
                        if fsize == 0:
                            os.remove(self.webm_path)
                            raise Exception("Target file size is %s" % fsize)
                        else:
                            os.remove(self.path)
                    except:
                        raise Exception(ffmpegresult)
                except:
                    raise Exception("FFmpeg polegl na konwertowaniu")

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        if os.path.exists(self.webm_path):
            os.remove(self.webm_path)
        super(ThumbnailVideoOrImageFieldFile, self).delete(save)

class ThumbnailVideoOrImageField(VideoOrImageField):
    attr_class = ThumbnailVideoOrImageFieldFile

    def __init__(self, thumb_width=230, thumb_height=161, thumb_aspect=True, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        self.thumb_aspect = thumb_aspect
        super(ThumbnailVideoOrImageField, self).__init__(*args, **kwargs)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([
    (
        [ThumbnailVideoOrImageField], # Class(es) these apply to
        [],         # Positional arguments (not used)
        {           # Keyword argument
            "thumb_width": ["thumb_width", {"default": 230}],
            "thumb_height": ["thumb_height", {"default": 161}],
            "thumb_aspect": ["thumb_aspect", {"default": True}],
        },
    ),
], ["^portfolio\.fields\.ThumbnailVideoOrImageField"])
