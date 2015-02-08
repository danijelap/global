import Image
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django.core.files.base import ContentFile

# other imports and models

class City(models.Model):
    # your fields

    def get_thumbnail(self, thumb_size=None):
        # find a way to choose one of the uploaded images and
        # assign it to `chosen_image`.
        base = Image.open(StringIO(chosen_image.image.read()))  # get the image

        size = thumb_size
        if not thumb_size:
            # set a default thumbnail size if no `thumb_size` is given
            rate = 0.2  # 20% of the original size
            size = base.size
            size = (int(size[0] * rate), int(size[1] * rate))

        base.thumbnail(size)  # make the thumbnail
        thumbnail = StringIO()
        base.save(thumbnail, 'PNG')
        thumbnail = ContentFile(thumbnail.getvalue())  # turn the tumbnail to a "savable" object
        return thumbnail