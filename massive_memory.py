import string

values = list(string.ascii_uppercase) + list(string.ascii_lowercase) + list(string.digits) + ['+', '/']
values_dict = {}

for i, v in enumerate(values):
  values_dict[i] = v

values = values_dict
del values_dict

def integer_to_massive_memory(num: int):
  count_4096 = num // 4096
  remainder = num % 4096
    
  count_64 = remainder // 64
  remainder = remainder % 64
    
  count_1 = remainder
    
  output = f'{values[count_1]}{values[count_64]}{values[count_4096]}'

  return output