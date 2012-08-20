from django.forms.fields import ImageField, ValidationError
from django.utils.translation import ugettext_lazy as _

from utils import is_video, is_video_buffer


class VideoOrImageField(ImageField):
    default_error_messages = {
        'invalid_video': _(u"Upload a valid video. The file you uploaded was either not an video or a corrupted file."),
    }

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports) or video.
        """
        f = super(ImageField, self).to_python(data)
        if f is None:
            return None

        file = None
        buffer = None

        # We need to get a file object. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                buffer = data.read()
            else:
                buffer = data['content']

        # If file is not vide, check if its an Image file
        if (file and not is_video(file)) or (buffer and not is_video_buffer(buffer)):
            f = super(VideoOrImageField, self).to_python(data)
            if f is None:
                return None

        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f
