import time

str = '2023-06-23'
t = time.strptime(str, '%Y-%m-%d')
print(time.strftime('%d.%m.%Y', t))
