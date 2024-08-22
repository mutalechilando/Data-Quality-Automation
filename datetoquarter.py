import datetime

def get_quarter(date_string):
  date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d')
  quarter = (date_obj.month - 1) // 3 + 1
  return f"{date_obj.year}Q{quarter}"

# Example usage:
date_str = "2022-08-01"
quarter_str = get_quarter(date_str)
print(quarter_str)  # Output: 2024Q3
