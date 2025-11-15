#!/usr/bin/env python3
"""
Convert Kaggle Visual Product Recognition dataset to products.json format
Usage: python scripts/convert_kaggle_dataset.py
"""

import json
import os
import kagglehub
from pathlib import Path
import csv
import random
import requests
from PIL import Image
from io import BytesIO

def download_dataset():
    """Download the Kaggle dataset"""
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("warcoder/visual-product-recognition")
    print(f"Dataset downloaded to: {path}")
    return path

def find_dataset_files(dataset_path):
    """Find CSV and image files in the dataset"""
    dataset_dir = Path(dataset_path)
    
    # Look for common file patterns
    csv_files = list(dataset_dir.glob("*.csv"))
    image_dirs = [d for d in dataset_dir.iterdir() if d.is_dir()]
    
    print(f"\nFound {len(csv_files)} CSV file(s)")
    print(f"Found {len(image_dirs)} image directory(ies)")
    
    if csv_files:
        print(f"CSV files: {[f.name for f in csv_files]}")
    if image_dirs:
        print(f"Image directories: {[d.name for d in image_dirs]}")
    
    return csv_files, image_dirs

def convert_to_products_json(dataset_path, output_path="public/data/products.json"):
    """
    Convert the Kaggle dataset to products.json format
    
    Customize this function based on your dataset structure:
    - If you have CSV with columns: adjust the column names below
    - If images are in folders: adjust the image path logic
    """
    
    csv_files, image_dirs = find_dataset_files(dataset_path)
    
    if not csv_files:
        print("\n⚠️  No CSV file found. Checking for alternative formats...")
        return convert_from_images_only(dataset_path, image_dirs, output_path)
    
    # Use the first CSV file found
    csv_file = csv_files[0]
    print(f"\nProcessing: {csv_file}")
    
    products = []
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        # Try to detect delimiter
        sample = f.read(1024)
        f.seek(0)
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        
        reader = csv.DictReader(f, delimiter=delimiter)
        
        # Print available columns for reference
        print(f"Available columns: {reader.fieldnames}")
        
        for idx, row in enumerate(reader, start=1):
            # ⚠️ CUSTOMIZE THESE COLUMN NAMES based on your CSV structure
            # Common column name variations:
            product_name = (
                row.get('name') or 
                row.get('product_name') or 
                row.get('title') or 
                row.get('product') or
                f"Product {idx}"
            )
            
            category = (
                row.get('category') or 
                row.get('class') or 
                row.get('label') or 
                row.get('type') or
                "General"
            )
            
            # Generate random price if not available
            price = float(row.get('price', random.randint(10, 500)))
            
            # Handle image path
            image_filename = (
                row.get('image') or 
                row.get('image_path') or 
                row.get('filename') or
                row.get('file') or
                f"image_{idx}.jpg"
            )
            
            # Convert local path to web-accessible path
            # Option 1: If images will be in public/images/
            image_path = f"/images/{Path(image_filename).name}"
            
            # Option 2: If using external hosting (uncomment and modify)
            # image_path = f"https://your-cdn.com/{Path(image_filename).name}"
            
            products.append({
                "id": idx,
                "name": product_name,
                "category": category,
                "price": price,
                "image": image_path
            })
            
            if idx % 100 == 0:
                print(f"Processed {idx} products...")
    
    # Save to JSON
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully converted {len(products)} products")
    print(f"📄 Saved to: {output_file}")
    print(f"\n📊 Sample product:")
    print(json.dumps(products[0], indent=2))
    
    # Print category summary
    categories = {}
    for p in products:
        categories[p['category']] = categories.get(p['category'], 0) + 1
    
    print(f"\n📦 Categories found: {len(categories)}")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {cat}: {count} products")
    
    return products

def convert_from_images_only(dataset_path, image_dirs, output_path):
    """
    Fallback: Create products.json from image files only
    Useful when no CSV metadata is available
    """
    print("\n🔄 Converting from image files only...")
    
    products = []
    idx = 1
    
    # Common image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    
    for image_dir in image_dirs:
        category = image_dir.name
        
        for img_file in image_dir.iterdir():
            if img_file.suffix.lower() in image_extensions:
                product_name = img_file.stem.replace('_', ' ').replace('-', ' ').title()
                
                products.append({
                    "id": idx,
                    "name": product_name,
                    "category": category,
                    "price": random.randint(10, 500),
                    "image": f"/images/{img_file.name}"
                })
                
                idx += 1
    
    if not products:
        print("❌ No images found in the dataset")
        return []
    
    # Save to JSON
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {len(products)} products from images")
    print(f"📄 Saved to: {output_file}")
    
    return products

def copy_images_to_public(dataset_path, image_dirs):
    """
    Optional: Copy images to public/images/ directory
    """
    print("\n📁 Copying images to public/images/...")
    
    public_images = Path("public/images")
    public_images.mkdir(parents=True, exist_ok=True)
    
    import shutil
    
    copied = 0
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    
    for image_dir in image_dirs:
        for img_file in image_dir.iterdir():
            if img_file.suffix.lower() in image_extensions:
                dest = public_images / img_file.name
                shutil.copy2(img_file, dest)
                copied += 1
                
                if copied % 100 == 0:
                    print(f"Copied {copied} images...")
    
    print(f"✅ Copied {copied} images to public/images/")
    return copied

def main():
    print("=" * 60)
    print("🔄 Kaggle Dataset to products.json Converter")
    print("=" * 60)
    
    # Step 1: Download dataset
    dataset_path = download_dataset()
    
    # Step 2: Convert to products.json
    products = convert_to_products_json(dataset_path)
    
    if not products:
        print("\n❌ Conversion failed. Please check the dataset structure.")
        return
    
    # Step 3: Optional - Copy images to public folder
    csv_files, image_dirs = find_dataset_files(dataset_path)
    
    if image_dirs:
        copy_choice = input("\n📥 Copy images to public/images/? (y/n): ").lower()
        if copy_choice == 'y':
            copy_images_to_public(dataset_path, image_dirs)
        else:
            print("\n💡 Remember to host images separately (Cloudinary/GitHub/imgix)")
            print(f"   Images are currently at: {dataset_path}")
    
    print("\n" + "=" * 60)
    print("✅ Conversion complete!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Review the generated public/data/products.json")
    print("2. If images are local, upload them to public/images/ or a CDN")
    print("3. Update image URLs in products.json if using external hosting")
    print("4. Test the app with the new dataset")

def merge_multiple_datasets():
    """Merge products from multiple Kaggle datasets"""
    datasets = [
        "warcoder/visual-product-recognition",
        # Add more datasets here for larger dataset:
        # "paramaggarwal/fashion-product-images-dataset",
        # "PromptCloudHQ/flipkart-products",
    ]
    
    all_products = []
    current_id = 1
    
    for dataset_name in datasets:
        print(f"\n{'='*60}")
        print(f"Processing: {dataset_name}")
        print('='*60)
        try:
            path = kagglehub.dataset_download(dataset_name)
            products = convert_to_products_json(path, "temp.json")
            
            # Adjust IDs and add to collection
            for p in products:
                p['id'] = current_id
                all_products.append(p)
                current_id += 1
            
            print(f"✓ Added {len(products)} products from {dataset_name}")
        except Exception as e:
            print(f"✗ Failed to process {dataset_name}: {e}")
    
    return all_products


def add_sample_products():
    """Add sample products with external images for testing"""
    categories = {
        'Electronics': ['laptop', 'headphones', 'camera', 'smartphone', 'tablet'],
        'Fashion': ['shoes', 'dress', 'jacket', 'watch', 'sunglasses'],
        'Home': ['furniture', 'lamp', 'decor', 'kitchenware', 'bedding'],
        'Sports': ['bicycle', 'running-shoes', 'yoga-mat', 'dumbbells', 'backpack'],
    }
    
    products = []
    idx = 1
    
    for category, items in categories.items():
        for item in items:
            for variant in range(3):
                products.append({
                    'id': idx,
                    'name': f"{item.replace('-', ' ').title()} Model {chr(65+variant)}",
                    'category': category,
                    'price': round(random.uniform(20, 800), 2),
                    'image': f"https://source.unsplash.com/400x400/?{item}&sig={idx}"
                })
                idx += 1
    
    return products


if __name__ == "__main__":
    print("=" * 60)
    print("Visual Product Matcher - Dataset Converter")
    print("=" * 60)
    print("\nOptions:")
    print("1. Convert single Kaggle dataset (default)")
    print("2. Merge multiple Kaggle datasets")
    print("3. Generate sample products with Unsplash images")
    print("4. Combine all (Kaggle + samples for max dataset)")
    
    choice = input("\nEnter choice (1-4) [1]: ").strip() or "1"
    
    try:
        if choice == "1":
            main()
        elif choice == "2":
            products = merge_multiple_datasets()
            if products:
                output_path = Path("public/data/products.json")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as f:
                    json.dump(products, f, indent=2)
                print(f"\n✅ Merged {len(products)} products")
                print(f"📁 Saved to: {output_path}")
        elif choice == "3":
            products = add_sample_products()
            output_path = Path("public/data/products.json")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(products, f, indent=2)
            print(f"\n✅ Generated {len(products)} sample products")
            print(f"📁 Saved to: {output_path}")
        elif choice == "4":
            print("\n🚀 Creating maximum dataset...\n")
            
            # Get Kaggle data
            kaggle_products = merge_multiple_datasets()
            
            # Add samples
            sample_products = add_sample_products()
            
            # Merge and deduplicate
            all_products = kaggle_products + sample_products
            
            # Remove duplicates
            seen = set()
            unique = []
            for p in all_products:
                key = f"{p['name']}_{p['category']}"
                if key not in seen:
                    seen.add(key)
                    p['id'] = len(unique) + 1
                    unique.append(p)
            
            output_path = Path("public/data/products.json")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(unique, f, indent=2)
            
            print(f"\n✅ Created maximum dataset with {len(unique)} products")
            print(f"📁 Saved to: {output_path}")
        else:
            print("Invalid choice, running default...")
            main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Tip: Customize column names based on your dataset")
        raise
