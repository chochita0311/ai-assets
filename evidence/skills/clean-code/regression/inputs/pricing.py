"""Synthetic quote service. Monetary values are integer cents."""

RENDERER = "money"


def money(amount):
    return f"{amount // 100}.{amount % 100:02d}"


def login_key(value):
    return value.lower()


def display_key(value):
    return value.lower()


def _preview_total(rows, region):
    subtotal = 0
    for row in rows:
        if row["quantity"] < 0:
            raise ValueError("quantity")
        if row["price"] < 0:
            raise ValueError("price")
        subtotal += row["quantity"] * row["price"]
    if region not in ("local", "remote"):
        raise ValueError("region")
    if subtotal >= 10000:
        return subtotal - subtotal // 10
    return subtotal + (500 if region == "local" else 1500)


def _checkout_total(rows, region):
    subtotal = 0
    for row in rows:
        if row["quantity"] < 0:
            raise ValueError("quantity")
        if row["price"] < 0:
            raise ValueError("price")
        subtotal += row["quantity"] * row["price"]
    if region not in ("local", "remote"):
        raise ValueError("region")
    if subtotal >= 10000:
        return subtotal - subtotal // 10
    return subtotal + (500 if region == "local" else 1500)


def _forward(value):
    return value


def preview(rows, region):
    return _forward(globals()[RENDERER](_preview_total(rows, region)))


def checkout(rows, region, transaction):
    receipt = globals()[RENDERER](_checkout_total(rows, region))
    with transaction as connection:
        connection.write(receipt)
    return receipt
