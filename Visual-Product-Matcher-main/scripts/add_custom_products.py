#!/usr/bin/env python3
"""
Add custom products to the dataset manually
Usage: python scripts/add_custom_products.py
"""

import json
from pathlib import Path

def load_existing_products():
    """Load existing products.json"""
    products_path = Path(__file__).parent.parent / 'public' / 'data' / 'products.json'
    
    if products_path.exists():
        with open(products_path, 'r') as f:
            return json.load(f)
    return []

def save_products(products):
    """Save products to products.json"""
    products_path = Path(__file__).parent.parent / 'public' / 'data' / 'products.json'
    products_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(products_path, 'w') as f:
        json.dump(products, f, indent=2)

def add_product_interactive():
    """Add a single product interactively"""
    products = load_existing_products()
    next_id = max([p['id'] for p in products], default=0) + 1
    
    print("\n" + "=" * 60)
    print("Add New Product")
    print("=" * 60)
    
    name = input("Product name: ").strip()
    category = input("Category: ").strip()
    price = float(input("Price ($): ").strip())
    image = input("Image URL or path (/images/...): ").strip()
    
    new_product = {
        'id': next_id,
        'name': name,
        'category': category,
        'price': price,
        'image': image
    }
    
    products.append(new_product)
    save_products(products)
    
    print(f"\n✅ Added product #{next_id}: {name}")
    print(f"📊 Total products: {len(products)}")

def add_products_from_csv(csv_file):
    """Add products from a CSV file"""
    import csv
    
    products = load_existing_products()
    next_id = max([p['id'] for p in products], default=0) + 1
    
    added = 0
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                new_product = {
                    'id': next_id,
                    'name': row.get('name', '').strip(),
                    'category': row.get('category', '').strip(),
                    'price': float(row.get('price', 0)),
                    'image': row.get('image', '').strip()
                }
                
                if new_product['name'] and new_product['image']:
                    products.append(new_product)
                    next_id += 1
                    added += 1
            except Exception as e:
                print(f"⚠️  Skipped row: {e}")
    
    save_products(products)
    print(f"\n✅ Added {added} products from CSV")
    print(f"📊 Total products: {len(products)}")

def bulk_add_from_template():
    """Add multiple products from a template"""
    products = load_existing_products()
    next_id = max([p['id'] for p in products], default=0) + 1
    
    print("\n" + "=" * 60)
    print("Bulk Add Products (Template Mode)")
    print("=" * 60)
    print("\nEnter products in format: name|category|price|image_url")
    print("One product per line. Enter empty line to finish.\n")
    print("Example:")
    print("iPhone 15|Electronics|999|https://example.com/iphone.jpg")
    print("Nike Shoes|Fashion|150|/images/shoes.jpg\n")
    
    new_products = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        
        try:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                new_products.append({
                    'id': next_id,
                    'name': parts[0],
                    'category': parts[1],
                    'price': float(parts[2]),
                    'image': parts[3]
                })
                next_id += 1
                print(f"  ✓ Added: {parts[0]}")
            else:
                print(f"  ✗ Invalid format (need 4 fields)")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    if new_products:
        products.extend(new_products)
        save_products(products)
        print(f"\n✅ Added {len(new_products)} new products")
        print(f"📊 Total products: {len(products)}")
    else:
        print("\nNo products added.")

def show_stats():
    """Show current dataset statistics"""
    products = load_existing_products()
    
    if not products:
        print("\n📭 No products in dataset")
        return
    
    categories = {}
    total_value = 0
    
    for p in products:
        category = p.get('category', 'Unknown')
        categories[category] = categories.get(category, 0) + 1
        total_value += p.get('price', 0)
    
    print("\n" + "=" * 60)
    print("Dataset Statistics")
    print("=" * 60)
    print(f"Total products: {len(products)}")
    print(f"Average price: ${total_value / len(products):.2f}")
    print(f"\nProducts by category:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("Visual Product Matcher - Custom Product Manager")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("1. Add single product (interactive)")
        print("2. Bulk add products (template)")
        print("3. Import from CSV file")
        print("4. Show dataset statistics")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            add_product_interactive()
        elif choice == "2":
            bulk_add_from_template()
        elif choice == "3":
            csv_file = input("Enter CSV file path: ").strip()
            if Path(csv_file).exists():
                add_products_from_csv(csv_file)
            else:
                print(f"❌ File not found: {csv_file}")
        elif choice == "4":
            show_stats()
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")
