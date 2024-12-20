import pytest
from bots.time_machine import bot
from bots.utils.analysis import calculate_returns

def test_calculate_returns():
    analysis = calculate_returns(
        entry_price=1000,
        current_price=1100,
        entry_time=1000,
        current_time=2000
    )
    assert analysis.profit_loss == 10.0
    assert analysis.time_held == 1000

def test_bot_state():
    # Test bot state initialization and updates
    pass