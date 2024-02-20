from decimal import Decimal as D

def line(times):
    """这个函数用来打印分割线
times即长度 "-" 的个数
无返回值"""
    for i in range(times):
        print("-", end = "")
    print()




while True :
    times = int(input("有几个数据："))
    all_ = 0        #data           所有输入数据之和
    all_2 = 0       #|xi - x_|            
    list1 = []      #data           存放所有数据
    list2 = []      #|di|           存放绝对偏差的绝对值
    list3 = []      #di             存放绝对偏差

    for i in range(times):
        x = i + 1
        print("请输入数据", x, "：", end = "")
        data = input()              #数据输入
        b = D(data)                 
        list1.append(b)             
        all_ += b
    
    pingjvn = all_ / times                      #平均数
    
    for i in range(times):
        Cha = list1[i] - pingjvn    #绝对偏差
        list2.append(abs(Cha))      
        all_2 += abs(Cha)           
        list3.append("%.4f" % Cha)  

    pjPianCha = all_2 / times                   #平均偏差
    xdpjPianCha = pjPianCha / pingjvn * 100     #相对平均偏差

    #打印部分
    print()
    line(20)
    print("平均数：       ", "%.4f" % pingjvn)
    print("绝对偏差di：   ", list3)
    print("平均偏差：     ", "%.4f" % pjPianCha)
    print("相对平均偏差： ", "%.4f" % xdpjPianCha, "%")
    line(20)
    print()
    end = input("-直接回车结束--输入任意键回车后继续-")
    if end:
        print()
        line(40)
        print()
        continue
    else:
        break

"""
line(15)
print("all_2", all_2)
print("list1：", list1)
print("list2：", list2)
line(15)
"""
