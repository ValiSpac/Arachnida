# Spider and Scorpion  

This project contains two programs: **Spider** and **Scorpion**.  

---

## Spider: Web Image Downloader  

**Spider** downloads images from a website, with options for recursive downloading and saving to a specific folder.  

### Usage  
```bash
./spider [-rlp] URL
```
### Options

    -r
    Recursively download images from the given URL.

    -r -l [N]
    Set the recursion depth (default: 5).

    -p [PATH]
    Save images to a specific directory (default: ./data/).

### Supported Image Formats

    .jpg / .jpeg
    .png
    .gif
    .bmp

## Scorpion: Image Metadata Extractor

**Scorpion** extracts and displays metadata from image files.
Usage
```bash
./scorpion FILE1 [FILE2 ...]
```
### Features

    Displays file attributes
    Example: creation date, file size, etc.

    Extracts EXIF metadata
    Information like camera details, geolocation , and more.(if available)
