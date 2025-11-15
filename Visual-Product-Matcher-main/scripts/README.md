# Dataset Management Scripts

Expand your Visual Product Matcher with more training data for better ML model performance.

## Available Scripts

### 1. `download_large_dataset.py` - **Best for Maximum Data** 🚀
Automatically downloads and merges 5+ large Kaggle datasets (1000+ products)

### 2. `convert_kaggle_dataset.py` - Custom Dataset Import
Convert specific Kaggle datasets with multiple merge options

### 3. `add_custom_products.py` - Manual Product Manager
Add, edit, and manage products interactively

---

## Quick Start

### ⚡ Recommended: Large Dataset (1000+ products)

```bash
# Install requirements first
pip install kagglehub pillow requests tqdm

# Download and merge multiple large datasets
python scripts/download_large_dataset.py
```

This creates a production-ready dataset automatically.

### Option A: Custom Kaggle Import

```bash
python scripts/convert_kaggle_dataset.py
# Choose option 4 for maximum dataset
```

### Option B: Add Products Manually

```bash
python scripts/add_custom_products.py
# Interactive menu for adding/managing products
```

---

## Why More Data Improves ML Accuracy

The CLIP vision model works better with:
- **Diverse products**: More categories = better generalization
- **Quality images**: Clear, high-resolution product photos
- **Varied angles**: Different views of similar products
- **Large dataset**: 500-1000+ products recommended for production

### Dataset Size Guide

| Size | Products | Use Case |
|------|----------|----------|
| Minimum | 50+ | Assignment requirement |
| Good | 200-500 | Testing & development |
| **Recommended** | **500-1000** | **Production deployment** |
| Optimal | 1000+ | Maximum accuracy |

---

## Detailed Usage

### convert_kaggle_dataset.py Options

**Option 1:** Single dataset conversion
**Option 2:** Merge multiple Kaggle datasets  
**Option 3:** Generate 60 sample products (Unsplash images)
**Option 4:** Combine Kaggle + samples (maximum)

### add_custom_products.py Features

Interactive menu with:
1. Add single product (guided prompts)
2. Bulk add (template: `name|category|price|image`)
3. Import from CSV
4. View dataset statistics

Example bulk add:
```
> iPhone 15|Electronics|999|https://example.com/phone.jpg
> Nike Shoes|Fashion|150|/images/shoes.jpg
```

---

## Expanding Your Dataset

### Strategy 1: Multiple Kaggle Datasets

Edit `convert_kaggle_dataset.py` line 256:

```python
datasets = [
    "warcoder/visual-product-recognition",
    "paramaggarwal/fashion-product-images-dataset",
    "PromptCloudHQ/flipkart-products",
    # Add more...
]
```

Then run option 2 (merge multiple).

### Strategy 2: Use `download_large_dataset.py` (Easiest)

Pre-configured with 5 high-quality datasets. Just run it!

### Strategy 3: Web Scraping (Advanced)

- Scrape e-commerce sites (respect robots.txt)
- Use APIs (Amazon, eBay, Shopify)
- Store images in `public/images/`
- Add metadata via `add_custom_products.py`

### Strategy 4: Public Image Datasets

Free sources:
- **Unsplash**: High-quality product photos
- **Pexels**: Free stock images
- **Pixabay**: Large image library

---

## Configuration & Customization

### CSV Column Mapping

Edit `convert_kaggle_dataset.py` if your CSV uses different columns:

### Image Hosting Options

**Option 1: Local (public/images/)**
- Good for: Small datasets (<100 images), development
- Run script with "y" when prompted to copy images

**Option 2: GitHub**
- Good for: Medium datasets, version control
- Commit images to repo, use `/images/filename.jpg` paths

**Option 3: Cloudinary/imgix**
- Good for: Large datasets, production, CDN benefits
- Upload images to CDN, update `image_path` logic in script

**Option 4: Keep Unsplash**
- Good for: Quick testing without real product images
- Use existing products.json

### Troubleshooting

**"No CSV file found"**
- The script will try to generate products.json from image filenames
- Categories will be based on folder structure

**"Column not found"**
- Check the printed column names
- Update the column mapping in `convert_to_products_json()`

**Large dataset**
- Consider limiting to first N products for testing
- Add this after the reader loop: `if idx > 1000: break`

### Example Output

```json
[
  {
    "id": 1,
    "name": "Nike Air Max Sneakers",
    "category": "Footwear",
    "price": 129.99,
    "image": "/images/nike-air-max.jpg"
  },
  ...
]
```
