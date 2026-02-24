def generate_rom(extracted_data, rate_card):
    """
    Generate Rough Order of Magnitude estimate
    
    Args:
        extracted_data: dict with timeline_months, complexity, etc.
        rate_card: dict with role rates
    
    Returns:
        dict with rom_hours and rom_cost
    """
    timeline = extracted_data.get("timeline_months", 1)
    complexity = extracted_data.get("complexity", "Medium")
    
    # Base calculation: 20 hours per month
    base_pm_hours = 20 * timeline
    
    # Complexity multiplier
    complexity_factor = {
        "Low": 0.8,
        "Medium": 1.0,
        "High": 1.3
    }
    
    multiplier = complexity_factor.get(complexity, 1.0)
    estimated_hours = base_pm_hours * multiplier
    
    # Calculate cost
    pm_rate = rate_card.get("Program Manager", 100)
    total_cost = estimated_hours * pm_rate
    
    return {
        "rom_hours": round(estimated_hours, 2),
        "rom_cost": round(total_cost, 2),
        "timeline_months": timeline,
        "complexity": complexity,
        "hourly_rate": pm_rate
    }