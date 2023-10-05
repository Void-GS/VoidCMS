import os
import random
from faker import Faker
from pathlib import Path

from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from voidcms.models import Category, Image, Product


def transliterate_cyrillic_to_latin(text):
    # Define a custom transliteration mapping for Cyrillic to Latin characters
    cyrillic_to_latin = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }

    # Transliterate the text character by character
    transliterated_text = ''
    for char in text:
        transliterated_text += cyrillic_to_latin.get(char, char)

    return transliterated_text


fake = Faker('ru_RU')
BASE_DIR = Path(__file__).resolve().parent.parent


# List of image filenames available in 'voidcms/faker/dummy' directory
IMAGE_FILES = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg',
               '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg', '11.jpg', '12.jpg']


def generate_dummy_data():
    # Create 17 categories
    categories = []
    for _ in range(32):
        words = fake.words(random.randint(1, 2))
        title = " ".join(words)
        uri = transliterate_cyrillic_to_latin("-".join(words))
        while Category.objects.filter(meta_url=uri).exists():
            uri = "-".join(words) + f"-{fake.random_number()}"
        category = Category.objects.create(
            title=title,
            description=fake.text(),
            image=gen_image(),
            meta_url=uri,
            meta_title=fake.sentence(),
            meta_description=fake.paragraph(),
            meta_keywords=fake.words(5),
        )
        category.save()
        categories.append(category)

    for _ in range(350):
        words = fake.words(random.randint(1, 4))
        title = " ".join(words)
        uri = transliterate_cyrillic_to_latin("-".join(words))
        while Product.objects.filter(meta_url=uri).exists():
            uri = "-".join(words) + f"-{fake.random_number()}"
        category = fake.random_element(categories)
        product = Product.objects.create(
            title=title,
            content=fake.paragraph(nb_sentences=random.randint(9, 16)),
            price=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            category=category,
            visible=True,
            is_promotioned=fake.pybool(),
            meta_url=uri,
            meta_title=fake.sentence(),
            meta_description=fake.paragraph(),
            meta_keywords=fake.words(5),
        )

        for _ in range(random.randint(2, 5)):
            product.images.add(gen_image())


def gen_image():
    image_filename = random.choice(IMAGE_FILES)
    image_path = os.path.join(BASE_DIR, 'faker', 'dummy', image_filename)

    img_temp = NamedTemporaryFile(delete=True)
    with open(image_path, 'rb') as f:
        img_temp.write(f.read())
    img_temp.flush()

    image = Image.objects.create(name=fake.word())
    image.url.save(image_filename, File(img_temp))
    return image
