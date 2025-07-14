# Price Scraper and Currency Converter
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt
import sys

class PriceScraper:
    """
    A web scraper class that extracts product information from websites
    and converts prices to different currencies using mock exchange rates.
    """
    
    def __init__(self, base_url="https://books.toscrape.com/"):
        """
        Initialize the scraper with a base URL and session configuration.
        
        Args:
            base_url (str): The website URL to scrape from
        """
        self.base_url = base_url
        
        # Create a session for making HTTP requests with custom headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Mock exchange rates (in real scenario, you'd use an API like exchangerate-api.com)
        # These rates represent the conversion from USD to other currencies
        self.exchange_rates = {
            'USD': 1.0,      # Base currency
            'KES': 150.0,    # 1 USD = 150 Kenyan Shillings
            'EUR': 0.85,     # 1 USD = 0.85 Euros
            'GBP': 0.73,     # 1 USD = 0.73 British Pounds
            'JPY': 110.0,    # 1 USD = 110 Japanese Yen
            'CAD': 1.25,     # 1 USD = 1.25 Canadian Dollars
            'AUD': 1.35,     # 1 USD = 1.35 Australian Dollars
            'INR': 75.0,     # 1 USD = 75 Indian Rupees
        }
    
    def get_exchange_rate(self, from_currency, to_currency):
        """
        Get exchange rate between two currencies using mock rates.
        
        Args:
            from_currency (str): Source currency code
            to_currency (str): Target currency code
            
        Returns:
            float: Exchange rate for conversion
        """
        try:
            # In a real implementation, you'd call an API like exchangerate-api.com
            # For now, we'll use mock rates stored in the class
            
            # If currencies are the same, return 1.0
            if from_currency == to_currency:
                return 1.0
            
            # Convert through USD as base currency
            # Get the rate from source currency to USD
            usd_from = self.exchange_rates.get(from_currency, 1.0)
            # Get the rate from USD to target currency
            usd_to = self.exchange_rates.get(to_currency, 1.0)
            
            # Calculate the cross-rate
            return usd_to / usd_from
            
        except Exception as e:
            print(f"Error getting exchange rate: {e}")
            return 1.0  # Return 1.0 as fallback
    
    def scrape_products(self, max_products=10):
        """
        Scrape product information from the website.
        
        Args:
            max_products (int): Maximum number of products to scrape
            
        Returns:
            list: List of dictionaries containing product information
        """
        products = []
        
        try:
            # Make HTTP request to the website
            print(f"Connecting to {self.base_url}...")
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all product containers on the page
            # The website uses 'article' tags with class 'product_pod' for each product
            product_containers = soup.find_all('article', class_='product_pod')
            
            print(f"Found {len(product_containers)} products on the page")
            
            # Extract information from each product container
            for i, container in enumerate(product_containers):
                if len(products) >= max_products:
                    break
                
                try:
                    # Extract product name from the h3 tag and its anchor link
                    name_element = container.find('h3').find('a')
                    product_name = name_element.get('title', 'Unknown Product')
                    
                    # Extract price from the price_color class
                    price_element = container.find('p', class_='price_color')
                    if price_element:
                        price_text = price_element.text.strip()
                        # Remove currency symbols and convert to float
                        # Books.toscrape.com uses GBP (£) as default currency
                        price_value = float(price_text.replace('£', '').replace('$', '').replace('€', ''))
                        original_currency = 'GBP'  # Books.toscrape uses GBP
                    else:
                        price_value = 0.0
                        original_currency = 'GBP'
                    
                    # Extract rating from the star-rating class
                    rating_element = container.find('p', class_='star-rating')
                    rating = rating_element.get('class')[1] if rating_element else 'No rating'
                    
                    # Extract availability information
                    availability_element = container.find('p', class_='availability')
                    availability = availability_element.text.strip() if availability_element else 'Unknown'
                    
                    # Create product dictionary with all extracted information
                    products.append({
                        'name': product_name,
                        'original_price': price_value,
                        'original_currency': original_currency,
                        'rating': rating,
                        'availability': availability
                    })
                    
                except Exception as e:
                    print(f"Error processing product {i+1}: {e}")
                    continue
            
            print(f"Successfully scraped {len(products)} products")
            return products
            
        except requests.RequestException as e:
            print(f"Connection error: {e}")
            return []
        except Exception as e:
            print(f"Error scraping products: {e}")
            return []
    
    def convert_prices(self, products, target_currency='KES'):
        """
        Convert prices from original currency to target currency.
        
        Args:
            products (list): List of product dictionaries
            target_currency (str): Currency code to convert prices to
            
        Returns:
            list: List of products with converted prices
        """
        converted_products = []
        timestamp = datetime.now().isoformat()  # Current timestamp for tracking
        
        print(f"Converting prices to {target_currency}...")
        
        for product in products:
            try:
                original_price = product['original_price']
                original_currency = product['original_currency']
                
                # Get exchange rate for conversion
                exchange_rate = self.get_exchange_rate(original_currency, target_currency)
                
                # Convert price using the exchange rate
                converted_price = original_price * exchange_rate
                
                # Create new product dictionary with converted price information
                converted_product = {
                    **product,  # Include all original product data
                    'converted_price': round(converted_price, 2),
                    'target_currency': target_currency,
                    'exchange_rate': round(exchange_rate, 4),
                    'conversion_timestamp': timestamp
                }
                
                converted_products.append(converted_product)
                
            except Exception as e:
                print(f"Error converting price for {product.get('name', 'Unknown')}: {e}")
                continue
        
        return converted_products
    
    def save_to_csv(self, products, filename=None):
        """
        Save products data to a CSV file using pandas.
        
        Args:
            products (list): List of product dictionaries
            filename (str): Name of the CSV file to save (optional)
        """
        try:
            # Generate filename with timestamp if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f'products_with_converted_prices_{timestamp}.csv'
            
            # Convert list of dictionaries to pandas DataFrame
            df = pd.DataFrame(products)
            # Save DataFrame to CSV file
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def save_to_json(self, products, filename=None):
        """
        Save products data to a JSON file.
        
        Args:
            products (list): List of product dictionaries
            filename (str): Name of the JSON file to save (optional)
        """
        try:
            # Generate filename with timestamp if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f'products_with_converted_prices_{timestamp}.json'
            
            # Write data to JSON file with proper formatting
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def display_table(self, products):
        """
        Display products in a formatted table using pandas.
        
        Args:
            products (list): List of product dictionaries to display
        """
        if not products:
            print("No products to display")
            return
        
        # Create a DataFrame for better display
        df = pd.DataFrame(products)
        
        # Select and rename columns for display
        display_df = df[['name', 'original_price', 'original_currency', 'converted_price', 'target_currency', 'rating', 'availability']].copy()
        
        # Truncate long product names for better display
        def truncate_name(name):
            return name[:50] + '...' if len(name) > 50 else name
        
        # Use list comprehension instead of map for better compatibility
        display_df['name'] = [truncate_name(name) for name in display_df['name']]
        
        # Format price columns for better readability
        display_df['original_price'] = display_df['original_price'].astype(str) + ' ' + display_df['original_currency']
        display_df['converted_price'] = display_df['converted_price'].astype(str) + ' ' + display_df['target_currency']
        
        # Drop the currency columns since they're now combined with prices
        display_df = display_df.drop(['original_currency', 'target_currency'], axis=1)
        
        # Rename columns for better display
        display_df.columns = ['Product Name', 'Original Price', 'Converted Price', 'Rating', 'Availability']
        
        # Display formatted table
        print("\n" + "="*100)
        print("PRODUCTS WITH CONVERTED PRICES")
        print("="*100)
        print(display_df.to_string(index=False))
        print("="*100)
    
    def plot_prices(self, products):
        """
        Create a bar chart comparing original vs converted prices using matplotlib.
        
        Args:
            products (list): List of product dictionaries with price information
        """
        if not products:
            print("No products to plot")
            return
        
        try:
            # Prepare data for plotting
            names = [product['name'][:20] + '...' if len(product['name']) > 20 else product['name'] 
                    for product in products]
            original_prices = [product['original_price'] for product in products]
            converted_prices = [product['converted_price'] for product in products]
            
            # Create the bar chart
            x = range(len(names))
            width = 0.35  # Width of the bars
            
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(15, 8))
            
            # Create bars for original and converted prices
            bars1 = ax.bar([i - width/2 for i in x], original_prices, width, 
                          label=f'Original ({products[0]["original_currency"]})', 
                          color='skyblue', alpha=0.8)
            bars2 = ax.bar([i + width/2 for i in x], converted_prices, width, 
                          label=f'Converted ({products[0]["target_currency"]})', 
                          color='lightcoral', alpha=0.8)
            
            # Customize the plot
            ax.set_xlabel('Products')
            ax.set_ylabel('Price')
            ax.set_title('Original vs Converted Prices')
            ax.set_xticks(x)
            ax.set_xticklabels(names, rotation=45, ha='right')
            ax.legend()
            
            # Add value labels on top of each bar
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f'{height:.2f}',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom', fontsize=8)
            
            # Adjust layout and save the plot with timestamp
            plt.tight_layout()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chart_filename = f'price_comparison_{timestamp}.png'
            plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
            print(f"Price comparison chart saved as '{chart_filename}'")
            
            # Display ASCII art representation in terminal
            print("\n" + "="*80)
            print("PRICE COMPARISON CHART (Terminal View)")
            print("="*80)
            
            for i, product in enumerate(products):
                name = product['name'][:30] + '...' if len(product['name']) > 30 else product['name']
                original = product['original_price']
                converted = product['converted_price']
                
                # Create simple bar representation using ASCII characters
                original_bars = '█' * int(original * 2)
                converted_bars = '█' * int(converted * 2)
                
                print(f"{i+1:2d}. {name}")
                print(f"    Original ({product['original_currency']}):  {original:6.2f} {original_bars}")
                print(f"    Converted ({product['target_currency']}): {converted:6.2f} {converted_bars}")
                print()
            
            print("="*80)
            
        except Exception as e:
            print(f"Error creating plot: {e}")

def main():
    """
    Main function to run the price scraper with user interaction.
    """
    print("🚀 Price Scraper & Currency Converter")
    print("="*50)
    
    # Initialize the scraper with default settings
    scraper = PriceScraper()
    
    # Get user preferences for currency and number of products
    print("\nAvailable currencies:", ", ".join(scraper.exchange_rates.keys()))
    target_currency = input("Enter target currency (default: KES): ").strip().upper() or 'KES'
    
    # Validate currency input
    if target_currency not in scraper.exchange_rates:
        print(f"Invalid currency. Using default: KES")
        target_currency = 'KES'
    
    # Get number of products to scrape
    max_products = input("Enter number of products to scrape (default: 10): ").strip()
    max_products = int(max_products) if max_products.isdigit() else 10
    
    # Display configuration
    print(f"\nScraping {max_products} products from {scraper.base_url}")
    print(f"Converting prices to {target_currency}")
    print("-" * 50)
    
    # Step 1: Scrape products from the website
    products = scraper.scrape_products(max_products)
    
    if not products:
        print("❌ No products found. Exiting...")
        return
    
    # Step 2: Convert prices to target currency
    converted_products = scraper.convert_prices(products, target_currency)
    
    if not converted_products:
        print("❌ Error converting prices. Exiting...")
        return
    
    # Step 3: Display results in a formatted table
    scraper.display_table(converted_products)
    
    # Step 4: Save data to files
    scraper.save_to_csv(converted_products)
    scraper.save_to_json(converted_products)
    
    # Step 5: Create visualization
    scraper.plot_prices(converted_products)
    
    # Success message
    print("\n✅ Price scraping and conversion completed successfully!")
    print(f"📊 Data saved to CSV and JSON files")
    print(f"📈 Price comparison chart saved as PNG")

if __name__ == "__main__":
    """
    Entry point of the script with error handling.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 