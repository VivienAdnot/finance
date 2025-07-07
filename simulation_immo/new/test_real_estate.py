import unittest
from real_estate import (
    calculate_annual_interest_payment,
    calculate_annual_deductible_expenses,
    calculate_taxes,
    calculate_loan_parameters,
    calculate_interest_payments,
    calculate_net_rental_income
)

class TestCalculateAnnualInterestPayment(unittest.TestCase):
    def test_first_year(self):
        loan_duration = 3
        interest_payments = [100] * 3 * 12  # 3 years of monthly interest payments
        year = 1

        result = calculate_annual_interest_payment(interest_payments, year, loan_duration)

        expected_payment = 1200  # 100 * 12
        self.assertEqual(result, expected_payment)

    def test_within_loan_duration(self):
        result = calculate_annual_interest_payment(
            loan_duration = 3,
            interest_payments = [100] * 3 * 12,  # 3 years of monthly interest payments
            year = 2,
        )

        expected_payment = 1200  # 100 * 12
        self.assertEqual(result, expected_payment)

    def test_exceeds_loan_duration(self):
        interest_payments = [100] * 36  # 3 years of monthly interest payments
        loan_duration = 3
        year = 4 # 4th year so 1 year after the loan duration

        result = calculate_annual_interest_payment(interest_payments, year, loan_duration)
        
        expected_payment = 0
        self.assertEqual(result, expected_payment)


class TestCalculateTaxes(unittest.TestCase):
    def test_calculate_taxes(self):
        maintenance = 168
        coownership_expense = 170 * 12
        interest_payment = 552.75 * 12
        deductible_expenses = calculate_annual_deductible_expenses(maintenance, coownership_expense, interest_payment)
        
        taxes = calculate_taxes(
            annual_rent=1400 * 12,
            deductible_expenses=deductible_expenses,
            income_tax_rate=30,
            social_charges_rate=17.2,
            property_tax=1100
        )
        self.assertEqual(round(taxes, 2), 4856.65)


# class TestCalculateLoanParameters(unittest.TestCase):
#     def test_calculate_loan_parameters(self):
#         loan_amount, monthly_payment = calculate_loan_parameters(
#             property_price=315000,
#             acquisition_fees=26000,
#             initial_cash=140000,
#             loan_rate=3.3,
#             loan_duration=20
#         )
#         self.assertEqual(loan_amount, 201000)
#         self.assertEqual(round(monthly_payment, 2), 1145.17)


# class TestCalculateInterestPayments(unittest.TestCase):
#     def test_calculate_interest_payments(self):
#         loan_amount, monthly_payment = calculate_loan_parameters(
#             property_price=315000,
#             acquisition_fees=26000,
#             initial_cash=140000,
#             loan_rate=3.3,
#             loan_duration=20
#         )
#         interest_payments, amortization_schedule = calculate_interest_payments(
#             loan_amount=loan_amount,
#             loan_rate=3.3,
#             loan_duration=20,
#             monthly_payment=monthly_payment
#         )
#         self.assertEqual(round(sum(interest_payments), 2), 73840.32)


class TestCalculateNetRentalIncome(unittest.TestCase):
    def test_calculate_net_rental_income(self):
        monthly_payment = 1145.17 # monthly payment to the bank
        annual_interest_payment = 552.75 * 12 # annual interest payment
        annual_maintenance_fee = 168
        annual_coownership_expense = 170 * 12

        deductible_expenses = calculate_annual_deductible_expenses(annual_maintenance_fee, annual_coownership_expense, annual_interest_payment)
        total_taxes = calculate_taxes(
            annual_rent=1400 * 12,
            deductible_expenses=deductible_expenses,
            income_tax_rate=30,
            social_charges_rate=17.2,
            property_tax=1100
        )
        net_rental_income = calculate_net_rental_income(
            annual_rent=1400 * 12,
            deductible_expenses=deductible_expenses,
            total_taxes=total_taxes,
            monthly_payment=1145.17,
            loan_duration=20,
            year=1
        )
        self.assertEqual(net_rental_income, -10639.688)


if __name__ == '__main__':
    unittest.main()