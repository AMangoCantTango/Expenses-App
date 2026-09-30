def split_cents(total, n):
    base, extra = divmod(total, n)
    return [base + (1 if i < extra else 0) for i in range(n)]


def balance(expenses, income):
    balances = {person: 0 for person in expenses}
    for e in income:
        balances[e['person']] += e['amount']
        shares = split_cents(e['amount'], len(e['expenses']))
        for person, share in zip(e['expenses'], shares):
            balances[person] -= share
    return balances


def settlement(balances):
    debtors = {n: -c for n, c in balances.items() if c < 0}
    creditors = {n: c for n, c in balances.items() if c > 0}
    payments = []
    while debtors and creditors:
        d = max(debtors, key=debtors.get)
        c = max(creditors, key=creditors.get)
        amount = min(debtors[d], creditors[c])
        payments.append((d, c, amount))
        creditors[c] -= amount
        if debtors[d] == 0:
            del debtors[d]
        if creditors[c] == 0:
            del creditors[c]
    return payments

def money(cents):
    return f"${abs(cents) / 100:.2f}"