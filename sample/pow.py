from hashlib import sha256

"""
プルーフ・オブ・ワークアルゴリズムの簡単な例
・ある整数xかけるある整数yのhashが0で終わらないといけない
"""

x = 5
y = 0  # まだこのyがどの数字であるべきかはわからない

while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1

print(f'The solution is y = {y}')
