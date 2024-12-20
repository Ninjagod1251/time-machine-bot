from dataclasses import dataclass
from typing import Optional
import pandas as pd

@dataclass
class TradeAnalysis:
    entry_price: float
    current_price: float
    time_held: int
    profit_loss: float
    
def calculate_returns(
    entry_price: Optional[float],
    current_price: float,
    entry_time: Optional[int],
    current_time: int
) -> Optional[TradeAnalysis]:
    """Calculate trading returns and metrics"""
    if not entry_price or not entry_time:
        return None
        
    profit_loss = ((current_price - entry_price) / entry_price) * 100
    
    return TradeAnalysis(
        entry_price=entry_price,
        current_price=current_price,
        time_held=current_time - entry_time,
        profit_loss=profit_loss
    )