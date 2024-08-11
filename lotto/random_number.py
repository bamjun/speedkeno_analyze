import os


# 1부터 45까지의 숫자를 생성하는 함수
def generate_random_number():
    # 16 바이트의 랜덤 바이트 생성
    random_bytes = os.urandom(1)

    # 바이트 데이터를 큰 정수로 변환
    random_int = int.from_bytes(random_bytes, byteorder="little")

    # 1부터 45 사이의 숫자로 매핑 (1 <= result <= 45)
    random_number = (random_int % 45) + 1

    return random_number


# 1부터 45까지의 랜덤 숫자 생성
# random_number = generate_random_number()
# print("Random number between 1 and 45:", random_number)

pickedNumber_list = []
while len(pickedNumber_list) != 6:
    random_number = generate_random_number()
    if not random_number in pickedNumber_list:
        pickedNumber_list.append(random_number)


print("Random number between 1 and 45:", sorted(pickedNumber_list))
