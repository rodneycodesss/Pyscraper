# Price Scraper & Currency Converter

A Python application that scrapes product prices from e-commerce websites and converts them to different currencies.

## Features

- 🌐 **Web Scraping**: Scrapes product information from https://books.toscrape.com/
- 💱 **Currency Conversion**: Converts prices between multiple currencies
- 📊 **Data Export**: Saves data in CSV and JSON formats
- 📈 **Visualization**: Creates bar charts comparing original vs converted prices
- 📋 **Table Display**: Shows results in formatted tables
- ⏰ **Timestamp**: Records when conversions were performed
- 🛡️ **Error Handling**: Robust error handling for network issues

## Supported Currencies

- USD (US Dollar)
- KES (Kenyan Shilling)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- CAD (Canadian Dollar)
- AUD (Australian Dollar)
- INR (Indian Rupee)

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the scraper:**
   ```bash
   python price_scraper.py
   ```

2. **Follow the prompts:**
   - Enter target currency (default: KES)
   - Enter number of products to scrape (default: 10)

3. **View results:**
   - Products displayed in formatted table
   - Data saved to CSV and JSON files
   - Price comparison chart saved as PNG
   - Terminal visualization of price comparisons

## Output Files

- `products_with_converted_prices.csv` - Product data in CSV format
- `products_with_converted_prices.json` - Product data in JSON format
- `price_comparison.png` - Bar chart comparing original vs converted prices

## Example Output

```
🚀 Price Scraper & Currency Converter
==================================================

Available currencies: USD, KES, EUR, GBP, JPY, CAD, AUD, INR
Enter target currency (default: KES): KES
Enter number of products to scrape (default: 10): 5

Scraping 5 products from https://books.toscrape.com/
Converting prices to KES
--------------------------------------------------
Successfully scraped 5 products

====================================================================================================
PRODUCTS WITH CONVERTED PRICES
====================================================================================================
| Product Name                    | Original Price | Converted Price | Rating    | Availability |
|================================|================|=================|===========|==============|
| A Light in the Attic           | 51.77 GBP     | 7568.21 KES     | Three     | In stock     |
| Tipping the Velvet             | 53.74 GBP     | 7852.02 KES     | One       | In stock     |
| Soumission                      | 50.10 GBP     | 7314.60 KES     | One       | In stock     |
| Sharp Objects                   | 47.82 GBP     | 6981.72 KES     | Four      | In stock     |
| Sapiens: A Brief History...     | 54.23 GBP     | 7917.58 KES     | Five      | In stock     |
====================================================================================================
```

## Features Implemented

✅ **Core Requirements:**
- Web scraping with requests and BeautifulSoup
- Price extraction and cleaning
- Currency conversion (mock rates)
- Data storage in CSV/JSON
- Table display with tabulate
- Error handling for connections

✅ **Optional Extensions:**
- User currency selection
- Timestamp for conversions
- Bar chart visualization with matplotlib
- Terminal display of price comparisons

## Technical Details

- **Web Scraping**: Uses requests for HTTP requests and BeautifulSoup for HTML parsing
- **Currency Conversion**: Mock exchange rates (can be replaced with real API)
- **Data Processing**: Pandas for data manipulation
- **Visualization**: Matplotlib for charts
- **Table Display**: Tabulate for formatted output

## Error Handling

The application includes robust error handling for:
- Network connection issues
- Invalid HTML parsing
- Missing product data
- Currency conversion errors
- File I/O operations

## Future Enhancements

- Integration with real currency exchange APIs
- Support for multiple e-commerce websites
- Historical price tracking
- Email notifications for price changes
- Web interface for easier interaction

## License

This project is open source and available under the MIT License. 