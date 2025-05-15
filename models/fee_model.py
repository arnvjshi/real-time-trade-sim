def calculate_fee(quantity_usd: float, fee_tier: float) -> float:
    """
    Rule-based fee calculation.
    - quantity_usd: Trade size in USD
    - fee_tier: fee rate as decimal (e.g., 0.001 for 0.1%)
    Returns total fee cost in USD.
    """
    fee = quantity_usd * fee_tier
    return fee
