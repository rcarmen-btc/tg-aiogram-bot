from re import A
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import googlemaps

with Image.open("inner.png").convert("RGBA") as inner:

    text = "צפפפפפפפפ"
    text1 = "פגי`צפ"
    text2 = "פ"

    # Flat for text
    inner_img = Image.new("RGBA", inner.size, (255, 255, 255, 0))
    inner_draw = ImageDraw.Draw(inner_img)

    # Fonts
    info_fnt = ImageFont.truetype("heebocyrillic.ttf", 65)
    price_fnt = ImageFont.truetype("heebocyrillic.ttf", 95)

    # Enter text
    inner_draw.text((760 - (len(text) * 40), 915), text, font=info_fnt, fill=(0, 0, 0, 255))
    inner_draw.text((760 - (len(text) * 40), 915 + 110), text, font=info_fnt, fill=(0, 0, 0, 255))
    inner_draw.text((760 - (len(text) * 40), 915 + 215), text, font=info_fnt, fill=(0, 0, 0, 255))
    inner_draw.text((760 - (len(text) * 40), 915 + 327), text, font=info_fnt, fill=(0, 0, 0, 255))
    inner_draw.text((510 - (len(text) * 40), 915 + 510), text1, font=price_fnt, fill=(81, 180, 227, 255))
    info = Image.alpha_composite(inner, inner_img)

    with Image.open("city.jpg") as background:

        # Add info card to blur background
        blur_background = background.resize((1080, 1920), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(radius=30))
        blur_background.paste(info, (65, 197))

        with Image.open("city.jpg") as photo:

            # Add photo
            fixed_city_width = 912
            fixed_city_heigth = 748
            height_percent = (fixed_city_heigth / float(photo.size[1]))
            height_size = int((float(photo.size[0]) * float(height_percent)))
            resized_photo = photo.resize((height_size, fixed_city_heigth)).crop((0, 0, fixed_city_width, fixed_city_heigth))
            blur_background.paste(resized_photo, (65 + 19, 197 + 19))

            # Add rectangle
            txt = Image.new("RGBA", (560, 100), (255, 255, 255, 0))
            blur_background.paste(txt, (261, 151))

            # Add price text
            draw = ImageDraw.Draw(blur_background)
            draw.text((560 - (len(text2) * 22), 161), text2, font=info_fnt, fill=(0, 0, 0, 255))
            blur_background.save('result.png')
