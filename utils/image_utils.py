import sys
from io import BytesIO
from PIL import Image, ImageOps, ExifTags

from django.core.files.uploadedfile import InMemoryUploadedFile


def image_compress(self, uploaded_image, add_watermark):
    image_temporary = Image.open(uploaded_image)
    good_image = ImageOps.exif_transpose(image_temporary)
    output_stream = BytesIO()
    image_temporary = good_image.convert("RGB")
    if image_temporary.size[0] > image_temporary.size[1]:
        image_temporary.thumbnail((768, 1024), Image.ANTIALIAS)
    else:
        image_temporary.thumbnail((1024, 768), Image.ANTIALIAS)

    # if add_watermark:
    #     image_temporary = add_thumbnail_logo(self, base_image=image_temporary)

    image_temporary.save(output_stream, format='JPEG', quality=70)
    output_stream.seek(0)
    self.thumbnail = InMemoryUploadedFile(output_stream, 'ImageField', "%s.jpg" % uploaded_image.name.split(
        '.')[0],
                                          'image/jpeg', sys.getsizeof(output_stream), None)


def rotate_image(uploaded_image):
    try:
        image = Image.open(uploaded_image)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image_name = uploaded_image.name.split('/')[-1]
        image.save(f"media/works/{image_name}")
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass


def add_thumbnail_logo(self, base_image):
    watermark = Image.open("logo.png")

    if base_image.size[0] > base_image.size[1]:
        watermark_width = base_image.size[0]
    else:
        watermark_width = base_image.size[1]

    watermark = watermark.resize((watermark_width, watermark_width), resample=Image.BICUBIC)
    base_image.paste(watermark, [0, 0], mask=watermark)

    return base_image


def add_photo_logo(self):
    base_image = Image.open(self.photo)
    watermark = Image.open('logo.png')

    if base_image.size[0] > base_image.size[1]:
        watermark_width = base_image.size[0]
    else:
        watermark_width = base_image.size[1]

    watermark = watermark.resize((watermark_width, watermark_width), resample=Image.BICUBIC)

    base_image.paste(watermark, (0, 0), mask=watermark)
    image_name = self.photo.name.split('/')[-1]
    base_image.save(f"media/works/{image_name}")
