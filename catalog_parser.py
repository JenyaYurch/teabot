import requests
from bs4 import BeautifulSoup
from db import Tea, Session
import re

def parse_catalog():
    url = "https://www.teashop.by/shop/china/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    teas = []
    for idx, product in enumerate(soup.select('.product-item')):
        # Debug: print product HTML
        print(f"\n--- Product {idx} HTML ---\n", product.prettify())
        # Name/title
        title_tag = product.select_one('div.title h3.title-container.product-titles')
        name = title_tag.get_text(strip=True) if title_tag else None
        # Debug: print name
        print(f"Name: {name}")
        # Price (robust extraction from nested bdi tag)
        price_tag = product.select_one('span.price span.woocommerce-Price-amount.amount bdi')
        print(f"Price tag: {price_tag}")
        price = price_tag.get_text(strip=True) if price_tag else None
        print(f"Extracted price: {price}")
        # Image
        image_div = product.select_one('div.image.mosaic-block.bar')
        image_tag = image_div.select_one('img') if image_div else None
        image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else None
        # Link
        link_tag = product.select_one('a')
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
        # Add link as description
        description = link
        teas.append({
            'name': name,
            'price': price,
            'image_url': image_url,
            'category': 'Китайский чай',
            'subcategory': None,
            'description': description,
            'packaging': None,
            'link': link
        })
    return teas

def update_database(teas):
    session = Session()
    for tea in teas:
        # Check if tea already exists by name and category
        existing = session.query(Tea).filter_by(name=tea['name'], category=tea['category']).first()
        if not existing:
            # Robust price extraction
            price_str = tea['price'] if tea['price'] else ''
            # Remove non-numeric prefixes (e.g., 'От', 'от', 'From', etc.)
            price_str = re.sub(r'^[^\d]*', '', price_str)
            # Remove currency and spaces
            price_str = price_str.replace('р.', '').replace('р', '').replace(',', '.')
            price_str = price_str.replace('\xa0', '').replace(' ', '').strip()
            # If price is a range (e.g., '6.00-8.00'), take the first value
            if '-' in price_str:
                price_str = price_str.split('-')[0].strip()
            try:
                price = float(price_str) if price_str else None
            except ValueError:
                price = None
            new_tea = Tea(
                name=tea['name'],
                category=tea['category'],
                subcategory=tea['subcategory'],
                description=tea['description'],
                price=price,
                packaging=tea['packaging'],
                image_url=tea['image_url']
            )
            session.add(new_tea)
    session.commit()
    session.close()