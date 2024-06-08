import variable

def calculate_cost_drone(days, distance_drone):
    # Calcul du coût pour les drones
    cost_drone_daily = days * variable.daily_drone_price
    cost_drone_distance = distance_drone * variable.distance_drone_price
    cost_drone_total = cost_drone_daily + cost_drone_distance

    return cost_drone_total

def calculate_cost_type_one(days, distance, nb_type_one):
    # Calcul du coût pour les véhicules de type 1
    distance_type_one = (distance / nb_type_one) * 2  # Division de la distance entre les deneigeuses
    cost_type_one_distance = distance_type_one * variable.distance_type_one_price
    time_type_one = distance_type_one / variable.speed_type_one
    cost_type_one_daily = days * variable.daily_type_one_price
    if (time_type_one > 8):
        cost_type_one_distance += (time_type_one - 8) * variable.extra_hour_type_one_price
    cost_type_one_total = (cost_type_one_distance + cost_type_one_daily) * nb_type_one

    return cost_type_one_total


def calculate_cost_type_two(days, distance, nb_type_two):
    # Calcul du coût pour les véhicules de type 2
    distance_type_two = (distance / nb_type_two) * 2  # Division de la distance entre les deneigeuses
    cost_type_two_distance = distance_type_two * variable.distance_type_two_price
    time_type_two = distance_type_two / variable.speed_type_two
    cost_type_two_daily = days * variable.daily_type_two_price
    if (time_type_two > 8):
        cost_type_two_distance += (time_type_two - 8) * variable.extra_hour_type_two_price
    cost_type_two_total = (cost_type_two_distance + cost_type_two_daily) * nb_type_two

    return cost_type_two_total

def calculate_cost_total(days, distance_drone, distance_type_one, distance_type_two):
    cost_drone_total = 0
    cost_type_one_total = 0
    cost_type_two_total = 0

    if (distance_drone > 0):
        cost_drone_total = calculate_cost_drone(days, distance_drone)

    if (distance_type_one > 0):
        cost_type_one_total = calculate_cost_type_one(days, distance_type_one, 4)

    if (distance_type_two > 0):
        cost_type_two_total = calculate_cost_type_two(days, distance_type_two, 4)

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