
async def count_callories(data):
    user_weight = data.get("weight")
    user_height = data.get("height")
    user_age = data.get("age")

    calories_norma = 10. * float(user_weight) + 6.25 * float(user_height) - 5. * float(user_age)
    return calories_norma