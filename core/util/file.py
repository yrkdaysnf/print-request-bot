from tqdm import tqdm
from pdf2image import convert_from_path as p2i
from PIL import Image

    
async def price_alg(pdf_path):
    popath = '.venv\\Lib\\site-packages\\poppler-23.11.0\\Library\\bin'
    fullness = 0.0
    images = p2i(pdf_path, grayscale=True,poppler_path=popath, dpi=50)
    pages = len(images)
    for img in tqdm(images, desc='Processing pages', unit='pages'):
        pixel=0.0
        w,h = img.size
        res=w*h
        for y in range(h):
            for x in range(w):
                pixel += 255-img.getpixel((x,y))
        if pixel == 0:
            pages = pages - 1
        else:
            pixel = pixel/255
        fullness += pixel/res
    return pages, fullness