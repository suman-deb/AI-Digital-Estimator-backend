
def generate_rom(extracted_data, rate_card):
    timeline = extracted_data.get("timeline_months", 1)
    complexity = extracted_data.get("complexity", "Medium")

    base_pm_hours = 20 * timeline

    complexity_factor = {
        "Low": 0.8,
        "Medium": 1.0,
        "High": 1.3
    }

    infra_factor = complexity_factor.get(complexity, 1.0)

    estimated_hours = base_pm_hours * infra_factor

    pm_rate = rate_card.get("Program Manager", 100)

    total_cost = estimated_hours * pm_rate

    return {
        "rom_hours": round(estimated_hours, 2),
        "rom_cost": round(total_cost, 2)
    }