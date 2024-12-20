FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY . .

# Environment variables
ENV PYTHONPATH=/app
ENV ALCHEMY_API_KEY=""
ENV ETHERSCAN_API_KEY=""

# Run the bot
CMD ["silverback", "run", "time_machine", "--network", "ethereum:mainnet:alchemy"]