@bot.on_(chain.blocks)
def track_prices(block):
    """Track token prices on each block"""
    try:
        # Add debug info
        print(f"Processing block {block.number}")
        
        # USDC/ETH Pair for price reference 
        USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        
        # Uniswap V3 Quoter
        QUOTER = Contract("0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6")

        for address, token in bot.state.data.tokens.items():
            try:
                # Get amount of USDC for 1 token
                quote = QUOTER.quoteExactInputSingle.call(
                    address,  # tokenIn
                    USDC,    # tokenOut
                    3000,    # fee (0.3%)
                    10**token.decimals,  # amount (1 token)
                    0        # sqrtPriceLimitX96
                )
                
                # Convert to USD price (USDC has 6 decimals)
                price = quote / 10**6
                
                print(f"Got price for {token.name}: ${price:.2f}")
                
                # Add to price history
                bot.state.data.price_history[address] = pd.concat([
                    bot.state.data.price_history[address],
                    pd.DataFrame([{
                        'timestamp': block.timestamp,
                        'price': price
                    }])
                ], ignore_index=True)
                
                # Calculate returns if we have an entry
                if address in bot.state.data.entry_points:
                    entry = bot.state.data.entry_points[address]
                    price_diff = price - entry['price']
                    profit_pct = (price_diff / entry['price']) * 100
                    time_held = block.timestamp - entry['timestamp']
                    
                    print(f"""
                    Time Machine Analysis for {token.name}:
                    Entry Price: ${entry['price']:.2f}
                    Current Price: ${price:.2f}
                    Time Held: {time_held // 86400} days, {(time_held % 86400) // 3600} hours
                    Hypothetical Profit/Loss: {profit_pct:.2f}%
                    """)
                    
            except Exception as e:
                print(f"Error getting price for {token.name}: {e}")
                continue
                
    except Exception as e:
        print(f"Error in price tracking: {e}")