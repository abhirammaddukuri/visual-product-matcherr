# Visual Product Matcher

An AI-powered visual search application that helps users find similar products by uploading images.

## Features

- **AI-Powered Image Matching**: Uses CLIP Vision Transformer for accurate visual similarity detection
- **Real-time Search**: Instantly analyzes uploaded images and finds matching products
- **Advanced Filtering**: Filter results by similarity score, category, and price range
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Smart Caching**: Optimized performance with intelligent embedding cache

## Technologies

This project is built with:

- **Frontend**: React 18 + TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **Build Tool**: Vite
- **AI/ML**: Hugging Face Transformers (CLIP Vision)
- **State Management**: React hooks

## Getting Started

### Prerequisites

- Node.js (v18 or higher recommended)
- npm or yarn

### Installation

```sh
# Clone the repository
git clone <YOUR_GIT_URL>

# Navigate to the project directory
cd visual-product-matcher

# Install dependencies
npm install

# Start the development server
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

```sh
# Create production build
npm run build

# Preview production build locally
npm run preview
```

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

## Deployment

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
