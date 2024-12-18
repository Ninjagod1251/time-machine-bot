from silverback import SilverbackBot
from ape import Contract, chain
import pandas as pd
from decimal import Decimal

# Initialize bot
bot = SilverbackBot()

class TokenConfig:
    def __init__(self, address: str, price_feed: str, decimals: int = 18, name: str = None):
        self.address = address
        self.price_feed = price_feed  # Chainlink price feed address
        self.decimals = decimals
        self.name = name or address[:8]

class TimeMachineState:
    def __init__(self):
        self.tokens = {}
        self.price_history = {}
        self.entry_points = {}
        self.position_sizes = {}  # Track number of tokens in each position
        self.initial_portfolio_value = 0
        self.current_portfolio_value = 0

def get_chainlink_price(price_feed_address: str) -> float:
    """Get price from Chainlink price feed"""
    try:
        price_feed = Contract(price_feed_address)
        latest_data = price_feed.latestRoundData()
        price = latest_data[1] / (10 ** price_feed.decimals())
        return price
    except Exception as e:
        raise Exception(f"Error getting Chainlink price: {e}")

@bot.on_startup()
def initialize_state(startup_state):
    """Initialize bot state and token tracking"""
    bot.state.data = TimeMachineState()
    
    # Example tokens to track with their Chainlink price feeds
    tokens_to_track = [
        TokenConfig(
            "0x514910771AF9Ca656af840dff83E8264EcF986CA",  # LINK
            "0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c",  # LINK/USD price feed
            18,
            "LINK"
        ),
        TokenConfig(
            "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",  # AAVE
            "0x547a514d5e3769680Ce22B2361c10Ea13619e8a9",  # AAVE/USD price feed
            18,
            "AAVE"
        ),
    ]
    
    for token in tokens_to_track:
        bot.state.data.tokens[token.address] = token
        bot.state.data.price_history[token.address] = pd.DataFrame(
            columns=['timestamp', 'price']
        )
        print(f"Initialized tracking for {token.name}")
    
    breakpoint()

@bot.on_(chain.blocks)
def track_prices(block):
    """Track token prices on each block"""
    try:
        print(f"\n=== Block {block.number} Analysis ===")
        total_current_value = 0
        
        breakpoint()
        
        for address, token in bot.state.data.tokens.items():
            try:
                price = get_chainlink_price(token.price_feed)
                
                # Update price history
                bot.state.data.price_history[address] = pd.concat([
                    bot.state.data.price_history[address],
                    pd.DataFrame([{
                        'timestamp': block.timestamp,
                        'price': price
                    }])
                ], ignore_index=True)
                
                # Calculate position value if we have an entry
                if address in bot.state.data.entry_points:
                    entry = bot.state.data.entry_points[address]
                    position_size = bot.state.data.position_sizes[address]
                    entry_value = entry['price'] * position_size
                    current_value = price * position_size
                    total_current_value += current_value
                    
                    price_diff = price - entry['price']
                    profit_pct = (price_diff / entry['price']) * 100
                    time_held = block.timestamp - entry['timestamp']
                    days = time_held // 86400
                    hours = (time_held % 86400) // 3600
                    
                    print(f"""
{token.name} Position:
  Size: {position_size} tokens
  Entry: ${entry['price']:.2f} (${entry_value:.2f})
  Current: ${price:.2f} (${current_value:.2f})
  P/L: {profit_pct:+.2f}% (${current_value - entry_value:+.2f})
  Time: {days}d {hours}h""")
                else:
                    print(f"\n{token.name} Price: ${price:.2f}")
                    
            except Exception as e:
                print(f"Error getting price for {token.name}: {e}")
                continue
        
        # Show portfolio summary if we have positions
        if bot.state.data.entry_points:
            total_pl = total_current_value - bot.state.data.initial_portfolio_value
            total_pl_pct = (total_pl / bot.state.data.initial_portfolio_value) * 100
            print(f"""
Portfolio Summary:
  Initial Value: ${bot.state.data.initial_portfolio_value:.2f}
  Current Value: ${total_current_value:.2f}
  Total P/L: {total_pl_pct:+.2f}% (${total_pl:+.2f})""")
                
    except Exception as e:
        print(f"Error in price tracking: {e}")

def add_new_token(address: str, price_feed: str, decimals: int = 18, name: str = None):
    """Add a new token to track"""
    if address in bot.state.data.tokens:
        print(f"Token {address} already being tracked")
        return
        
    token = TokenConfig(address, price_feed, decimals, name)
    bot.state.data.tokens[address] = token
    bot.state.data.price_history[address] = pd.DataFrame(
        columns=['timestamp', 'price']
    )
    print(f"Started tracking {token.name}")

def set_entry_point(token_address: str, position_size: float = 1.0):
    """Set current price as entry point for a token with position size"""
    if token_address not in bot.state.data.tokens:
        print(f"Token {token_address} not being tracked")
        return
        
    if len(bot.state.data.price_history[token_address]) > 0:
        current_price = bot.state.data.price_history[token_address].iloc[-1]['price']
        bot.state.data.entry_points[token_address] = {
            'price': current_price,
            'timestamp': chain.blocks.head.timestamp
        }
        bot.state.data.position_sizes[token_address] = position_size
        token_name = bot.state.data.tokens[token_address].name
        
        # Update initial portfolio value
        bot.state.data.initial_portfolio_value += current_price * position_size
        
        print(f"Entry set for {token_name}")
        print(f"Position: {position_size} tokens at ${current_price:.2f} = ${position_size * current_price:.2f}")
    else:
        print("No price data available yet")

def show_tracking_status():
    """Show all tokens being tracked"""
    for address, token in bot.state.data.tokens.items():
        entry = bot.state.data.entry_points.get(address)
        latest_price = None
        if len(bot.state.data.price_history[address]) > 0:
            latest_price = bot.state.data.price_history[address].iloc[-1]['price']
            
        print(f"""
        Token: {token.name}
        Address: {address}
        Price Feed: {token.price_feed}
        Latest Price: ${latest_price:.2f} if latest_price else 'No data'
        Entry Point: {'Yes' if entry else 'No'}
        """)