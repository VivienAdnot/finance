import numpy as np
import math
from datetime import date

def get_3_max_values(arr):
  np_array = np.array(arr)
  sorted_index_array = np.argsort(np_array)
  sorted_array = np_array[sorted_index_array]

  indices = sorted_index_array[-3:]
  result = sorted_array[-3:]
  return indices, result

# compute arithmetic average of array
# average(arg1, arg2, arg3)
def average(*args):
  return round(sum(args) / len(args), 2)

# compute variation between 2 prices
# https://www.schoolmouv.fr/formules/taux-de-variation/formule-ses
def compute_percentage_gain(value_current, value_previous):
  return round((value_current - value_previous) / value_previous * 100, 2)

def convert_to_year(number):
  return math.floor(number / 12)

def convert_to_year_15_years_ago(number):
  year_index = convert_to_year(number)
  return date.today().year - 15 + year_index

def convert_to_month(number):
  return number % 12

def convert_month_index_to_string(month_index):
  return date(1900, month_index, 1).strftime('%B')

# month must be between 1 and 12
def increment_month(month):
  return month + 1 if month < 12 else 1