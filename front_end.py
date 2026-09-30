import streamlit as stream

from Expenses_App import balance, money, settlement

stream.set_page_config(page_title="MoneySplit")
stream.title("MoneySplit")

if "people" not in stream.session_state:
    stream.session_state.people = []
    stream.session_state.expenses = []

people = stream.session_state.people
expenses = stream.session_state.expenses


stream.header("1. Group Members")
with stream.form(key="member_form"):
    member_name = stream.text_input("Member Name")
    if stream.form_submit_button("Add Member"):
        member_name = member_name.strip()
        if member_name and member_name not in people:
            people.append(member_name)
            stream.rerun()
stream.write(', '.join(people) if people else "No members added yet.")

stream.header("2. Add Expense")
if len(people) < 1:
    stream.info("Add at least one person to the group.")
else:
    with stream.form("add_expense_form", clear_on_submit=True):
        description = stream.text_input("Expense Description")
        amount = stream.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
        payer = stream.selectbox("Payer", people)
        among = stream.multiselect("Split Among", people, default = people)
        if stream.form_submit_button("Add Expense"):
            cents = round(amount * 100)
            if not description.strip() or cents <= 0 or not among:
                stream.error("Please fill in all fields correctly.")
            else:
                expenses.append({"description": description, "person": payer, "amount": cents, "expenses": among})
                stream.rerun()

stream.header("3. Expenses")
if not expenses:
    stream.caption("No expenses have been added.")
for i, e in enumerate(expenses):
    left, right = stream.columns([5, 1])
    left.write(f"**{e['description']}**: {money(e['amount'])} (Paid by {e['person']})")
    if right.button ("Delete", key=f"delete_{i}"):
        expenses.pop(i)
        stream.rerun()


if people:
    balances = balance(people, expenses)

    stream.header("4. Balances")
    for person in people:
        c = balances[person]
        if c > 0:
            stream.write(f"**{person}** is owed {money(c)}")
        elif c < 0:
            stream.write(f"**{person}** owes {money(c)}")
        else:
            stream.write(f"**{person}** has no balance.")

    stream.header("Who pays who")
    payments = settlement(balances)
    if not payments:
        stream.success("Everyone is even!")
    for payer, payee, amount in payments:
        stream.write(f"**{payer}** pays **{payee}** {money(amount)}")

if stream.button("Reset Group"):
    stream.session_state["people"] = []
    stream.session_state["expenses"] = []
    stream.rerun()