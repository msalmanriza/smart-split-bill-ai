def calculate_split(items):

    result = {}

    for item in items:

        person = item["payer"]
        amount = item["total_price"]

        result[person] = (
            result.get(person, 0)
            + amount
        )

    return result