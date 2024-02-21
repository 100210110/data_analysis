from decimal import Decimal as D

while True:
    num_list = []
    x = input("请输入Q检测法待测值: ")
    if x == "q":
        break

    while x:
        num_list.append(D(x))
        x = input("请输入Q检测法待测值: ")


    if num_list:
        # 排序
        sorted(num_list)

        q0 = max(num_list) - min(num_list)
        a = num_list[1] - min(num_list)
        b = max(num_list) - num_list[-2]
        q1 = max(a , b)
        Q1 = q1 / q0
        print(f"Q1 = {Q1} \n请和表中数据对比")
    else:
        print("输入为空")