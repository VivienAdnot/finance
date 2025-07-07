import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

def calculate_real_estate_capital_gains_tax(purchase_price, notary_fees, sale_price, holding_period):
    # Compute the gross capital gain
    acquisition_price = purchase_price + notary_fees
    gross_capital_gain = sale_price - acquisition_price

    # Compute applicable deductions
    if holding_period < 6:
        deduction_ir = 0
        deduction_ps = 0
    elif holding_period < 21:
        deduction_ir = (holding_period - 5) * 6
        deduction_ps = (holding_period - 5) * 1.65
    elif holding_period == 21:
        deduction_ir = 16 * 6  # 96%
        deduction_ps = (16 * 1.65) + 1.6  # 26.0%
    elif holding_period == 22:
        deduction_ir = 100  # Fully exempt from income tax
        deduction_ps = (17 * 1.65) + 1.6  # 27.6%
    elif 22 < holding_period < 30:
        deduction_ir = 100  # Fully exempt from income tax
        deduction_ps = 27.6 + ((holding_period - 22) * 9) # 36.6%
    else:
        deduction_ir = 100  # Fully exempt from both taxes
        deduction_ps = 100

    # Compute taxable capital gain
    taxable_capital_gain_ir = gross_capital_gain * (1 - deduction_ir / 100)
    taxable_capital_gain_ps = gross_capital_gain * (1 - deduction_ps / 100)

    # Compute taxes
    income_tax = taxable_capital_gain_ir * 0.19
    social_contributions = taxable_capital_gain_ps * 0.172
    total_tax = income_tax + social_contributions

    return total_tax

def calculate_loan_parameters(property_price, acquisition_fees, initial_cash, loan_rate, loan_duration):
    loan_amount = property_price + acquisition_fees - initial_cash

    monthly_rate = (loan_rate / 100) / 12
    loan_duration_in_months = loan_duration * 12
    
    if loan_amount > 0:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** loan_duration_in_months) / ((1 + monthly_rate) ** loan_duration_in_months - 1)
    else:
        monthly_payment = 0
    
    return loan_amount, monthly_payment

def calculate_interest_payments(loan_amount, loan_rate, loan_duration, monthly_payment):
    monthly_rate = (loan_rate / 100) / 12
    capital_remaining = loan_amount
    interest_payments = []
    amortization_schedule = []
    
    for _ in range(loan_duration * 12):
        interest = capital_remaining * monthly_rate
        principal_payment = monthly_payment - interest
        interest_payments.append(interest)
        amortization_schedule.append(capital_remaining)
        capital_remaining -= principal_payment
        if capital_remaining <= 0:
            break
    
    return interest_payments, amortization_schedule

def calculate_annual_interest_payment(interest_payments, year, loan_duration):
    """
    Calculate the total interest payment for a specific year of the loan.

    Parameters:
    interest_payments (list): List of monthly interest payments.
    year (int): The year for which to calculate the interest payment.
    loan_duration (int): The total duration of the loan in years.

    Returns:
    int: The total interest payment for the specified year, or 0 if the year exceeds the loan duration.
    """
    if year > loan_duration:
        return 0

    start_index = (year - 1) * 12
    end_index = year * 12

    annual_interest_payment = sum(interest_payments[start_index:end_index])

    return annual_interest_payment

def calculate_annual_deductible_expenses(maintenance, coownership_expense, interest_payment):
    return maintenance + coownership_expense + interest_payment

def calculate_taxes(annual_rent, deductible_expenses, income_tax_rate, social_charges_rate, property_tax):
    taxable_income = max(0, annual_rent - deductible_expenses)
    print(f"taxable_income: {taxable_income}")

    income_tax = taxable_income * (income_tax_rate / 100)
    social_charges = taxable_income * (social_charges_rate / 100)

    print(f"income_tax: {income_tax}, social_charges: {social_charges}")
    total_taxes = income_tax + social_charges + property_tax
    return total_taxes

def calculate_net_rental_income(annual_rent, deductible_expenses, total_taxes, monthly_payment, loan_duration, year):
    net_rental_income = annual_rent - deductible_expenses - total_taxes
    if year <= loan_duration:
        net_rental_income -= monthly_payment * 12
    return net_rental_income

def calculate_net_selling_price(sell_price, selling_fees):
    return sell_price * (1 - (selling_fees / 100))

def simulate_investment():
    print("Simulation de l'investissement en cours...")
    # Variables initiales
    property_price = 315000
    acquisition_fees = 26000
    down_payment = 140000
    years = 20
    # Loan
    loan_rate = 3.3
    loan_duration = years
    # Rental
    monthly_rental_income = 1400
    monthly_rent_increase = 10 # 10€ increase per month
    # Expenses
    maintenance_cost = 1
    monthly_coownership_fees = 170
    # Taxes
    income_tax_rate = 30
    social_charges_rate = 17.2
    property_tax = 1100
    property_tax_increase = 2
    # Property appreciation
    property_appreciation = 1
    # Selling
    selling_fees = 0
    
    loan_amount, monthly_payment = calculate_loan_parameters(property_price, acquisition_fees, down_payment, loan_rate, loan_duration)

    print(f"loan_amount: {loan_amount}, monthly_payment: {monthly_payment}")
    interest_payments, amortization_schedule = calculate_interest_payments(loan_amount, loan_rate, loan_duration, monthly_payment)
    
    current_property_value = property_price
    total_cash_invested = down_payment

    # when we start, the roi is the difference between the property value and the cash invested
    price_i_got = calculate_net_selling_price(property_price, selling_fees)
    money_i_owe = amortization_schedule[0]
    money_i_spent = down_payment
    print(f"price_i_got: {price_i_got}, money_i_owe: {money_i_owe}, money_i_spent: {money_i_spent}")
    roi = price_i_got - money_i_spent - money_i_owe
    print(f"roi when we start: {roi}")
    
    data = []
    annual_rent = (monthly_rental_income + monthly_rent_increase) * 12
    print(f"annual_rent: {annual_rent}")
    maintenance = annual_rent * (maintenance_cost / 100)
    print(f"maintenance: {maintenance}")
    annual_coownership_expense = monthly_coownership_fees * 12
    print(f"annual coownership_expense: {annual_coownership_expense}")

    for year in range(1, years + 1):
        print(f"====== Année {year} =======")
        interest_payment = calculate_annual_interest_payment(interest_payments, year, loan_duration)
        print(f"interest_payment: {interest_payment}")

        deductible_expenses = calculate_annual_deductible_expenses(
            maintenance,
            annual_coownership_expense,
            interest_payment)

        print(f"annual deductible_expenses: {deductible_expenses}")
        
        total_taxes_annual = calculate_taxes(
            annual_rent,
            deductible_expenses,
            income_tax_rate,
            social_charges_rate,
            property_tax)

        print(f"total_taxes: {total_taxes_annual}")
        
        final_net_rental_income_annual = calculate_net_rental_income(
            annual_rent,
            deductible_expenses,
            total_taxes_annual,
            monthly_payment,
            loan_duration,
            year)

        print(f"net_rental_income after loan payment: {final_net_rental_income_annual}")
        
        # when net_rental_income is negative, we need to add additional contribution
        additional_contribution = abs(final_net_rental_income_annual) if final_net_rental_income_annual < 0 else 0
        total_cash_invested += additional_contribution

        current_property_value *= (1 + property_appreciation / 100)
        property_tax *= (1 + property_tax_increase / 100)
        
        remaining_principal = amortization_schedule[year * 12 - 1] if year * 12 - 1 < len(amortization_schedule) else 0
        print(f"remaining_principal: {remaining_principal}")

        # the price we sell the property for, after selling fees
        net_selling_price = calculate_net_selling_price(current_property_value, selling_fees)
        # we have to pay when we sell the property
        tax_selling = calculate_real_estate_capital_gains_tax(
            purchase_price=property_price,
            notary_fees=acquisition_fees,
            sale_price=net_selling_price,
            holding_period=year)
        print(f"tax_selling: {tax_selling}")

        price_i_got = calculate_net_selling_price(current_property_value, selling_fees)
        money_i_owe = remaining_principal + tax_selling
        money_i_spent = total_cash_invested
        roi = price_i_got - money_i_spent - money_i_owe
        print(f"roi: {roi}")
        
        data.append([year, roi])
    
    return data

def run_simulation():
    data = simulate_investment()

    df = pd.DataFrame(data, columns=['Année', 'roi'])
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["Année"], df['roi'], label='roi')
    plt.xlabel("Années")
    plt.ylabel("Valeur (€)")
    plt.legend()
    plt.title("Évolution de la Valeur de l'Investissement")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    run_simulation()
