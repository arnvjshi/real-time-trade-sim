import math

def almgren_chriss_impact(order_size, daily_volume, volatility, time_horizon=1):
    """
    Calculate expected market impact cost using Almgren-Chriss model.
    
    Parameters:
    - order_size: size of the trade (USD)
    - daily_volume: average daily traded volume (USD)
    - volatility: daily volatility (decimal, e.g., 0.02 for 2%)
    - time_horizon: time to execute the order in days (default 1)
    
    Returns:
    - market impact cost in USD
    """
    # Permanent impact coefficient
    gamma = 0.1  
    # Temporary impact coefficient
    eta = 0.01  
    
    X = order_size
    V = daily_volume
    sigma = volatility
    T = time_horizon
    
    if V == 0:
        return 0
    
    # Impact model from Almgren & Chriss (simplified)
    permanent_impact = gamma * sigma * (X / V)
    temporary_impact = eta * (X / V) ** 2
    
    total_impact = (permanent_impact + temporary_impact) * X
    return total_impact
