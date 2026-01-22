from .base import BackgroundService

class FinanceService(BackgroundService):
    def __init__(self, config):
        self.base_currency = config.get("base_currency", "TRY")
        self.currencies = config.get("currencies", ["USD", "EUR"])
        self.show_gold = config.get("show_gold", True)
        super().__init__(update_interval=3600) # 1 hour

    def fetch_data(self):
        data = {}
        import requests
        
        try:
            url = "https://finans.truncgil.com/today.json"
            # Fake User-Agent to avoid blocks
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            resp = requests.get(url, headers=headers, timeout=20)
            
            if resp.status_code == 200:
                json_data = resp.json()
                
                # Helper to clean price: "34,50" -> 34.50; "1.200,50" -> 1200.50
                def clean_price(val_str):
                    try:
                        # Remove thousands separator (.) and replace decimal separator (,) with dot
                        cleaned = val_str.replace(".", "").replace(",", ".")
                        return float(cleaned)
                    except:
                        return 0.0

                # Currencies
                for curr in self.currencies:
                    if curr in json_data:
                        # Use 'Satış' (Selling) price
                        price_str = json_data[curr].get("Satış", "0")
                        data[curr] = clean_price(price_str)
                
                # Gold
                if self.show_gold and "gram-altin" in json_data:
                    price_str = json_data["gram-altin"].get("Satış", "0")
                    data["GOLD"] = clean_price(price_str)
            
            return data
                    
        except Exception as e:
            print(f"Finance API Error: {e}")
            return None

    def get_data(self):
        return super().get_data()
