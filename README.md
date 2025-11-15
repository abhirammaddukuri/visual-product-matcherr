# Project Overview
Visual Product Matcher — AI-Powered Image Similarity Engine

This project is a production-ready Visual Product Matching system that identifies visually similar products based on an uploaded image or image URL.
It uses deep-learning embeddings, vector similarity search, and an optimized React + Vercel frontend to deliver fast and accurate results.

The system is aimed at real-world e-commerce workflows such as:

Visual product recommendation

Similar product search

Duplicate product detection

Catalog enrichment and product tagging

The entire stack is optimized for speed, accuracy, and user experience.

# Home page after deploying in Vercel
<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/49f7fb8b-c63c-4f0f-8204-ade5f27f2a16" />

#  workflow after deploying project
<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/c0c4ad96-a61d-4e55-8283-a098d1764f71" />
<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/762460c4-f5e6-4504-8735-c4dadbe227ba" />

Model is working accuratly after deploying.

# Tech Stack (Very Professional Section)

# Machine Learning
CLIP (OpenAI) or MobileNetV2 for image embeddings
NumPy for vector normalization and similarity computation
FAISS / Annoy (optional) for optimized vector search

# Frontend
React (TypeScript)
Tailwind CSS
Dropzone for image upload
Vercel for hosting

# visual-product-matcherr

```sh
# Clone the repository
git clone (https://github.com/abhirammaddukuri/visual-product-matcherr)

# Navigate to the project directory
cd visual-product-matcherr

# Install dependencies
npm install

# Start the development server
npm run dev
```

The application will be available at `[https://visual-product-matcher-beta-roan.vercel.app/]`

## Building for Production

```sh
# Create production build
npm run build

# Preview production build locally
npm run preview
```
# Matching Algorithm Explanation 

Each image is resized, normalized, and converted into a consistent tensor format.
A pretrained model (CLIP/MobileNet) extracts the embedding vector representing the visual content.
All product images also have precomputed embeddings stored in JSON.

The system computes cosine similarity between the query embedding and every product embedding:

score = (1 - cosine_distance) * 100

The top-K highest scoring matches are sorted and displayed.

A threshold slider allows the user to filter low-similarity results.

# How It Works 

[User Image] 
      ↓
[Preprocessing & Normalization]
      ↓
[Embedding Model (CLIP / MobileNet)]
      ↓
[Feature Vector: 512/1024-D]
      ↓
[Cosine Similarity Search]
      ↓
[Top-K Product Matches]
      ↓
[Rendered Results + Similarity Score]

## Project Structure

```
├── src/
│   ├── components/      # React components
│   ├── hooks/           # Custom React hooks
│   ├── pages/           # Page components
│   ├── utils/           # Utility functions
│   └── lib/             # Library configurations
├── public/
│   └── data/           # Product dataset
└── scripts/            # Data management scripts
```
# Dataset Description

The system uses a dataset of 50+ product images across categories including:
Shoes, Shirts, Watches, Bags, Accessories, Electronics (optional)

The production build can be deployed to any static hosting service:

- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Any other static hosting provider

## Adding Custom Products

Use the provided Python scripts in the `scripts/` directory:

```sh
# Add products interactively
python scripts/add_custom_products.py

# Import from CSV
python scripts/add_custom_products.py --csv your_products.csv
```

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
 
 # Contact / Author Info
 Author: Sai Abhiram  
 B.Tech CSE (AI)  
 Email: maddukurisaiabhiram@gmail.com

