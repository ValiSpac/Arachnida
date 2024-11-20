import argparse
import pathlib
import exif
from PIL import Image
from PIL.ExifTags import TAGS

EXT = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

def get_info(image):
    info_dict = {
        "Filename": image.filename,
        "Image size": image.size,
        "Image height": image.height,
        "Image width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }
    for label, value in info_dict.items():
        print(f'{label:25}: {value}')

def parse_exif(image):
    try:
        img = Image.open(image)
        get_info(img)
        exifdata = img._getexif()
        if exifdata is None:
            print(f'No EXIF data found for the image {image}')
            return
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode()
            print(f'{tag:25}: {data}')
    except Exception as e:
        print(f'Problem reading the image {image}: {e}')


def main():
    parser=argparse.ArgumentParser(description='Extract and display EXIF metadata')
    parser.add_argument('files', type=pathlib.Path ,nargs='+', help='List of images to extract exif data')
    args = parser.parse_args()
    for file in args.files:
        if file.suffix not in EXT or not file.is_file():
            parser.error(f'{file} is not an available image')
        parse_exif(file)


if __name__=='__main__':
    main()
