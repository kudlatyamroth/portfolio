import magic, re
from django.forms.fields import FileField, ValidationError
from django.utils.translation import ugettext_lazy as _
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

HEADER = 4096
mime = magic.Magic(mime=True)
video_re = re.compile("^video\/.+")

def is_video(path):
    type = mime.from_file(path)
#    return video_re.match(type) != None
    return (video_re.match(type) != None) | (type == "application/octet-stream")

def is_video_buffer(buffer):
    type = mime.from_buffer(buffer)
#    return video_re.match(type) != None
    return (video_re.match(type) != None) | (type == "application/octet-stream")

class VideoOrImageField(FileField):
    default_error_messages = {
        'invalid_videoorimage': _(u"Upload a valid video or image. The file you uploaded was either not an video or image or a corrupted file."),
    }

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports, or video file).
        """
        f = super(VideoOrImageField, self).to_python(data)
        if f is None:
            return None

        file = None
        buffer = None

        # We need to get a file object for PIL. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                buffer = data.read()
            else:
                buffer = data['content']

        if file:
            if not is_video(file):
                # Try to import PIL in either of the two ways it can end up installed.
                try:
                    from PIL import Image
                except ImportError:
                    import Image

                try:
                    # load() is the only method that can spot a truncated JPEG,
                    #  but it cannot be called sanely after verify()
                    trial_image = Image.open(file)
                    trial_image.load()

                    # Since we're about to use the file again we have to reset the
                    # file object if possible.
                    if hasattr(file, 'reset'):
                        file.reset()

                    # verify() is the only method that can spot a corrupt PNG,
                    #  but it must be called immediately after the constructor
                    trial_image = Image.open(file)
                    trial_image.verify()
                except ImportError:
                    # Under PyPy, it is possible to import PIL. However, the underlying
                    # _imaging C module isn't available, so an ImportError will be
                    # raised. Catch and re-raise.
                    raise
                except Exception: # Python Imaging Library doesn't recognize it as an image
                    raise ValidationError(self.error_messages['invalid_videoorimage'])
        elif buffer:
            if not is_video_buffer(buffer):
                # Try to import PIL in either of the two ways it can end up installed.
                try:
                    from PIL import Image
                except ImportError:
                    import Image

                buffer = StringIO(buffer)

                try:
                    # load() is the only method that can spot a truncated JPEG,
                    #  but it cannot be called sanely after verify()
                    trial_image = Image.open(buffer)
                    trial_image.load()

                    # Since we're about to use the file again we have to reset the
                    # file object if possible.
                    if hasattr(buffer, 'reset'):
                        buffer.reset()

                    # verify() is the only method that can spot a corrupt PNG,
                    #  but it must be called immediately after the constructor
                    trial_image = Image.open(buffer)
                    trial_image.verify()
                except ImportError:
                    # Under PyPy, it is possible to import PIL. However, the underlying
                    # _imaging C module isn't available, so an ImportError will be
                    # raised. Catch and re-raise.
                    raise
                except Exception: # Python Imaging Library doesn't recognize it as an image
                    raise ValidationError(self.error_messages['invalid_videoorimage'])

        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f
