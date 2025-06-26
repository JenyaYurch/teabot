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
        # Description from details
        details_tag = product.select_one('div.details')
        description = details_tag.get_text(strip=True) if details_tag else None
        # Weight from attribute_pa_ves (inside form.variations_form)
        form_tag = product.select_one('form.variations_form')
        weight = None
        if form_tag and form_tag.has_attr('data-product_variations'):
            import json
            try:
                variations = json.loads(str(form_tag['data-product_variations']))
                if variations and isinstance(variations, list):
                    raw_weight = variations[0].get('attributes', {}).get('attribute_pa_ves')
                    # Extract only the first number from the weight string (e.g., '10g', '1sht-7gr')
                    if raw_weight:
                        match = re.search(r'(\d+)', raw_weight)
                        weight = int(match.group(1)) if match else None
            except Exception as e:
                print(f"Error parsing weight: {e}")
        # Product ID from data-product_id (on form)
        product_id = form_tag['data-product_id'] if form_tag and form_tag.has_attr('data-product_id') else None
        # Link
        link_tag = product.select_one('a')
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
        teas.append({
            'name': name,
            'price': price,
            'image_url': image_url,
            'category': 'Китайский чай',
            'subcategory': None,
            'description': description,
            'packaging': None,
            'link': link,
            'weight': weight,
            'product_id': product_id
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
                image_url=tea['image_url'],
                link=tea.get('link'),
                weight=tea.get('weight'),
                product_id=tea.get('product_id')
            )
            session.add(new_tea)
    session.commit()
    session.close()