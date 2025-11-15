#!/usr/bin/env python3
"""
Download and prepare large-scale product datasets
Combines multiple sources for maximum ML training data
"""

import kagglehub
import json
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Large Kaggle datasets for e-commerce/products
RECOMMENDED_DATASETS = [
    "warcoder/visual-product-recognition",
    "paramaggarwal/fashion-product-images-dataset", 
    "PromptCloudHQ/flipkart-products",
    "cclark/product-item-data",
    "vikashrajluhaniwal/fashion-images",
]

def download_all_datasets():
    """Download all recommended datasets"""
    print("🚀 Downloading large-scale datasets...\n")
    
    downloaded_paths = []
    
    for i, dataset in enumerate(RECOMMENDED_DATASETS, 1):
        print(f"[{i}/{len(RECOMMENDED_DATASETS)}] Downloading {dataset}...")
        try:
            path = kagglehub.dataset_download(dataset)
            downloaded_paths.append((dataset, path))
            print(f"  ✓ Downloaded to: {path}\n")
        except Exception as e:
            print(f"  ✗ Failed: {e}\n")
    
    return downloaded_paths

def process_all_datasets(downloaded_paths):
    """Process all downloaded datasets into unified format"""
    import csv
    import random
    
    all_products = []
    current_id = 1
    
    for dataset_name, path in downloaded_paths:
        print(f"\n📊 Processing {dataset_name}...")
        dataset_products = []
        
        # Try to find and parse CSV files
        for csv_file in Path(path).rglob("*.csv"):
            try:
                with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Extract product info with fallbacks
                        name = (row.get('name') or 
                               row.get('product_name') or 
                               row.get('productDisplayName') or 
                               row.get('title') or 
                               'Product')
                        
                        category = (row.get('category') or 
                                   row.get('masterCategory') or 
                                   row.get('class') or 
                                   row.get('articleType') or
                                   'General')
                        
                        # Try to parse price
                        price = None
                        for price_key in ['price', 'actual_price', 'discountedPrice', 'retail_price']:
                            if price_key in row and row[price_key]:
                                try:
                                    price_str = str(row[price_key]).replace('$', '').replace(',', '').strip()
                                    price = float(price_str)
                                    break
                                except:
                                    continue
                        
                        if not price:
                            price = round(random.uniform(10, 500), 2)
                        
                        # Get image path/URL
                        image = (row.get('image') or 
                                row.get('img') or 
                                row.get('link') or
                                row.get('image_url') or
                                '')
                        
                        if image and name:
                            dataset_products.append({
                                'id': current_id,
                                'name': name[:100],  # Truncate long names
                                'category': category,
                                'price': price,
                                'image': image,
                                'source': dataset_name.split('/')[1]
                            })
                            current_id += 1
                            
                            # Limit products per dataset to avoid memory issues
                            if len(dataset_products) >= 500:
                                break
                
                if len(dataset_products) >= 500:
                    break
                    
            except Exception as e:
                print(f"  ⚠️  Error processing {csv_file.name}: {e}")
        
        # If no CSV data, try images
        if not dataset_products:
            for img_file in Path(path).rglob("*"):
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                    category = img_file.parent.name
                    dataset_products.append({
                        'id': current_id,
                        'name': img_file.stem.replace('_', ' ').replace('-', ' ').title()[:100],
                        'category': category if category != 'images' else 'General',
                        'price': round(random.uniform(10, 500), 2),
                        'image': f"/images/{img_file.name}",
                        'source': dataset_name.split('/')[1]
                    })
                    current_id += 1
                    
                    if len(dataset_products) >= 500:
                        break
        
        print(f"  ✓ Extracted {len(dataset_products)} products")
        all_products.extend(dataset_products)
    
    return all_products

def deduplicate_products(products):
    """Remove duplicate products based on name and category"""
    seen = set()
    unique = []
    
    for product in products:
        key = f"{product['name'].lower()}_{product['category'].lower()}"
        if key not in seen:
            seen.add(key)
            product['id'] = len(unique) + 1  # Re-assign IDs
            unique.append(product)
    
    return unique

def save_dataset(products, filename='products.json'):
    """Save products to JSON file"""
    output_path = Path(__file__).parent.parent / 'public' / 'data' / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove 'source' field for cleaner output
    clean_products = []
    for p in products:
        clean = {k: v for k, v in p.items() if k != 'source'}
        clean_products.append(clean)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(clean_products, f, indent=2)
    
    print(f"\n✅ Saved {len(clean_products)} products to: {output_path}")
    return output_path

def show_dataset_stats(products):
    """Display statistics about the dataset"""
    categories = {}
    sources = {}
    total_value = 0
    
    for p in products:
        cat = p.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
        
        src = p.get('source', 'Unknown')
        sources[src] = sources.get(src, 0) + 1
        
        total_value += p.get('price', 0)
    
    print("\n" + "=" * 60)
    print("📊 DATASET STATISTICS")
    print("=" * 60)
    print(f"Total products: {len(products)}")
    print(f"Average price: ${total_value/len(products):.2f}")
    print(f"\nTop 10 categories:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        print(f"  • {cat}: {count}")
    print(f"\nSources:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  • {src}: {count}")

if __name__ == "__main__":
    print("=" * 60)
    print("Large-Scale Product Dataset Builder")
    print("=" * 60)
    print("\nThis will download and process 5+ large datasets")
    print("⚠️  This may take 10-30 minutes and use several GB of disk space\n")
    
    proceed = input("Continue? (y/n): ").lower().strip()
    
    if proceed == 'y':
        # Download all datasets
        paths = download_all_datasets()
        
        if not paths:
            print("\n❌ No datasets downloaded successfully")
            exit(1)
        
        # Process all datasets
        print("\n" + "=" * 60)
        products = process_all_datasets(paths)
        
        # Deduplicate
        print("\n🔄 Removing duplicates...")
        unique_products = deduplicate_products(products)
        print(f"  ✓ Kept {len(unique_products)} unique products (removed {len(products) - len(unique_products)} duplicates)")
        
        # Show stats
        show_dataset_stats(unique_products)
        
        # Save
        save_dataset(unique_products)
        
        print("\n" + "=" * 60)
        print("✨ Dataset ready for Visual Product Matcher!")
        print("=" * 60)
    else:
        print("\n👋 Cancelled")
