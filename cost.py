import variable

def calculate_cost(days, hours_type_one, hours_type_two, distance_drone):
    # Calcul du coût pour les drones
    cost_drone_daily = days * variable.daily_drone_price
    cost_drone_distance = distance_drone * variable.distance_drone_price
    cost_drone_total = cost_drone_daily + cost_drone_distance

    # Calcul du coût pour les véhicules de type 1
    distance_type_one = (variable.total_distance - distance_drone) / 2  # Supposons une répartition égale des distances
    cost_type_one_distance = distance_type_one * variable.distance_type_one_price
    time_type_one = distance_type_one / variable.speed_type_one
    cost_type_one_daily = days * variable.daily_type_one_price
    cost_type_one_hours = variable.first_hour_type_one_price * time_type_one
    if (time_type_one > 8):
        cost_type_one_hours += (time_type_one - 8) * variable.extra_hour_type_one_price
    cost_type_one_total = min(cost_type_one_daily, cost_type_one_distance, cost_type_one_hours)

    # Calcul du coût pour les véhicules de type 2
    distance_type_two = (variable.total_distance - distance_drone) / 2
    cost_type_two_distance = distance_type_two * variable.distance_type_two_price
    time_type_two = distance_type_two / variable.speed_type_two
    cost_type_two_daily = days * variable.daily_type_two_price
    cost_type_two_hours = variable.first_hour_type_two_price * time_type_two
    if (time_type_two > 8):
        cost_type_two_hours += (time_type_two - 8) * variable.extra_hour_type_two_price
    cost_type_two_total = min(cost_type_two_daily, cost_type_two_distance, cost_type_two_hours)

    # Coût total combiné
    total_cost = cost_drone_total + cost_type_one_total + cost_type_two_total

    # Vérification du budget
    if total_cost > variable.global_budget:
        return f"Le coût total ({total_cost}) dépasse le budget global ({variable.global_budget})."
    else:
        return {
            "Coût total": total_cost,
            "Coût Drone": cost_drone_total,
            "Coût Type 1": cost_type_one_total,
            "Coût Type 2": cost_type_two_total,
        }