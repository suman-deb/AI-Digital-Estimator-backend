
def evaluate_formula(formula, variables):
    allowed_names = variables.copy()
    return eval(formula, {"__builtins__": None}, allowed_names)

def generate_detailed_estimate(extracted_data, asset_template, rate_card):

    variables = {
        "data_volume_tb": extracted_data.get("data_volume_tb", 1),
        "estimated_users": extracted_data.get("estimated_users", 100),
        "timeline_months": extracted_data.get("timeline_months", 1)
    }

    base_effort = evaluate_formula(
        asset_template["base_effort_formula"],
        variables
    )

    breakdown = []
    total_cost = 0

    for role_info in asset_template["roles"]:
        role = role_info["role"]
        multiplier = role_info["multiplier"]

        role_hours = base_effort * multiplier
        rate = rate_card.get(role, 100)

        role_cost = role_hours * rate
        total_cost += role_cost

        breakdown.append({
            "role": role,
            "hours": round(role_hours, 2),
            "rate": rate,
            "cost": round(role_cost, 2)
        })

    return {
        "base_effort_hours": round(base_effort, 2),
        "breakdown": breakdown,
        "total_cost": round(total_cost, 2)
    }