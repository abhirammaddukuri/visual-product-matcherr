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
