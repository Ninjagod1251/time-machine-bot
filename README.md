# Time Machine Bot

A Silverback bot that tracks hypothetical crypto positions and answers the question "What if I had (not) sold?"
Made by Ninjagod1251

## Overview

Time Machine Bot helps you track and analyze hypothetical crypto trading positions. It enables you to:

- Track real-time prices for multiple tokens using Chainlink price feeds
- Set entry points with custom position sizes  
- Monitor hypothetical profits/losses
- Track total portfolio value
- Analyze what would have happened if you had held/sold positions

## Features

- Real-time price tracking using Chainlink oracles
- Support for multiple tokens and positions
- Portfolio-level tracking and analysis 
- Docker support for easy deployment
- Configurable position sizes
- Time-held tracking for each position
- Clear performance metrics

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)
- Alchemy API Key
- Etherscan API Key

## Installation

1. Clone the repository:
```bash
git clone <your-rep-url>
cd time-machine-bot
```

##  Docker Files

Docker Optional
Create a virtual environment (optional, not needed for Docker):

```python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

# Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:

`cp .env.example .env`

1. Edit `.env` and add your API keys:

```bash
envCopyALCHEMY_API_KEY=your_alchemy_key_here
ETHERSCAN_API_KEY=your_etherscan_key_here
```

# Running the Bot
Local Development
```bash
silverback run time_machine --network ethereum:mainnet:alchemy
Using Docker
bashCopy# Build and run
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f
```

# Bot Commands
When running the bot, you can use these commands at the breakpoint:

```python
# Add a new token to track
add_new_token(
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",  # Token address
    "0x553303d460EE0afB37EdFf9bE42922D8FF63220e",  # Price feed address
    name="UNI"
)

# Set an entry point with position size
set_entry_point('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', 100)  # Track 100 UNI

# Show tracking status
show_tracking_status()
```

# Example Output
```bash
Copy=== Block 21425878 Analysis ===

LINK Position:
  Size: 10 tokens
  Entry: $27.72 ($277.20)
  Current: $27.72 ($277.20)
  P/L: +0.00% ($0.00)
  Time: 0d 1h

AAVE Position:
  Size: 1 tokens  
  Entry: $358.60 ($358.60)
  Current: $358.60 ($358.60)
  P/L: +0.00% ($0.00)
  Time: 0d 1h

UNI Position:
  Size: 100 tokens
  Entry: $16.39 ($1,639.00)
  Current: $16.39 ($1,639.00)
  P/L: +0.00% ($0.00)
  Time: 0d 1h

Portfolio Summary:
  Initial Value: $2,274.80
  Current Value: $2,274.80
  Total P/L: +0.00% ($0.00)
```

# Project Structure

```bash
time-machine-bot/
├── .dockerignore
├── .env                  # API keys and configuration  
├── Dockerfile
├── ape-config.yaml      # Ape configuration
├── bots/
│   └── time_machine.py  # Main bot code
├── docker-compose.yml
└── requirements.txt
```

# Contributing

1. Fork the repository
2. .Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

# License

This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments

Silverback - The trading bot framework
ApeWorX - The development framework
Chainlink - Price feed oracles