print("正在载入请稍等……")
import importlib
import subprocess

# 需要安装的Python库
required_libraries = ['numpy', 'decimal', 'scipy', 'colorama']

# 未安装库的列表
missing_libraries = []



# 分割线
class line:
    # 直接打印
    def p(length):
        print('-' * length)
    
    # 返回值
    def r(length):
        return '-' * length


# 确认库是否安装
def is_library_installed(library_name):
    try:
        importlib.import_module(library_name)
        return True
    except ImportError:
        return False


# 检查tqdm进度条库并且安装
def test_tqmd():
    if not is_library_installed('tqdm'):
        print("tqdm进度条未安装, 正在尝试使用pip安装...")
        command = 'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple tqdm'
        subprocess.call(command, shell=True)


# 检查所有库是否安装, 并且把未安装库添加到missing_libraries列表中
def test_library():
    for library in required_libraries:
        print(f"\n正在检测 {library} 库")
        if not is_library_installed(library):
            missing_libraries.append(library)
            print(f"{library} 库未安装")
        else:
            print(f"{library} 库已经安装")


# 安装缺失库
def install_missing_lirary():
    if missing_libraries:
        for library in tqdm(missing_libraries, desc='Installing Libraries'):
            print(f'\n{library}库没有安装, 正在尝试使用pip安装...')
            command = f'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple {library}'
            subprocess.call(command, shell=True)
        print("依赖库已经全部安装完成。")
        print(f"{line.r(20)}\n\n{line.r(20)}")
    else:
        print("\n依赖库已经全部安装好。")
        print(f"{line.r(20)}\n\n{line.r(20)}")
    

# 检查所需库
if __name__ == '__main__':
    print("正在载入请稍等……")
    test_tqmd()
    from tqdm import tqdm
    test_library()
    install_missing_lirary()
    # input("\n<按任意键结束检查>\n")



import signal
import sys
import numpy as np
from decimal import Decimal as D
from scipy.stats import t
import functools



# 中断信号处理方法
def signal_handler(signal, frame):
    # 屏幕提示的文本可以根据个人兴趣设置
    print("\n (输入已保存, 按“e”键退出, 任意键继续) ", end="")
    # 清空数据并等待下一轮输入
    global nums
    # nums.clear()
    while True:
        try:
            choice = input()
            if choice.lower() == "e":
                sys.exit(0)
            else:
                break
        except KeyboardInterrupt:
            continue


# 取有效位数
class keep_digits:
    def  p(num, n = 4):
        print(f"{num:.{n}g}")
        return
    
    def  r(num, n = 4):
        return f"{num:.{n}g}"
    

# 数据处理
def data_analysis():
    global nums
    nums = []
    sum_nums = 0
    sum_squares = 0

    # data_analysis() 中注册信号处理方法，为ctrl+c处理办法
    # signal.signal(signal.SIGINT, functools.partial(signal_handler))
    while True:
        try:
            data = input("请输入数据 (按回车键结束): ")
            if not data:
                break

            try:
                num = D(data)
            except:
                print(f'“{data}”不是数字吧, 再看一眼？')
                continue

            nums.append(num)
            sum_nums += num

        except KeyboardInterrupt:
            print("检测到中断，输入已保存")
            signal_handler(None, None)  # 将参数修改为 (None, None)

    # 校验数据数量，为0或1拒绝处理
    n = len(nums)
    if n == 0:
        print("喂喂喂, 你没输入数据！")
        return
    elif n == 1:
        print("一个数字可不能拿来分析, 再整几个来")
        return

    mean = np.mean(nums)
    abs_deviations = np.abs(np.array(nums) - D(f"{mean:.4g}"))
    avg_abs_deviation = np.mean(abs_deviations)
    rel_std_dev, variance, std_dev = None, None, None
    if mean == 0:
        rel_avg_abs_deviation = 0 if avg_abs_deviation == 0 else float("inf")
    else:
        rel_avg_abs_deviation = avg_abs_deviation / mean * 100
    line.p(20)
    print(f"平均数:       {mean:.4g}")
    print(f"绝对偏差di:   {[f'{d:.4g}' for d in abs_deviations]}")
    print(f"平均偏差:     {avg_abs_deviation:.4g}")
    print(f"相对平均偏差: {rel_avg_abs_deviation:.2g} %")
    if sum_nums == 0:
        print("标准偏差:     和为0, 无法计算")
        print("相对标准偏差: 和为0, 无法计算")
        print("方差:         和为0, 无法计算")
    else:
        std_dev = np.std(nums)
        rel_std_dev = std_dev / mean * 100
        variance = np.var(nums)
        print(f"标准偏差:     {std_dev:.4g}")
        print(f"相对标准偏差: {rel_std_dev:.4g} %")
        print(f"方差:         {variance:.4g}")


    while True:
        if sum_nums == 0:
            print("置信区间:     和为0, 无法计算")
            break

        try:
            conf_level = input('\n请输入置信度 (0-100), 或按回车键跳过:')
            if conf_level == '':
                break
            conf_level = float(conf_level)
        except ValueError:
            print("再看一眼, 你输入的好像确实不是数字")
            continue

        if not (0 < conf_level < 100):
            print("置信区间诶老哥, 麻烦输入0到100之间的数")
            continue

        t_value = t.ppf((conf_level/100 + 1)/2, n-1)
        lower_ci = mean - D(t_value) * std_dev / D(n).sqrt()
        upper_ci = mean + D(t_value) * std_dev / D(n).sqrt()
        print(f"{conf_level}% 置信区间:[{lower_ci:.4g}, {upper_ci:.4g}]")
        break

    line.p(20)
    return


# 感谢函数，弄着玩的
def thanks():
    if count == 3 or (count > 0 and count % 5 == 0):
        print("\n-------------------------------------------")
        print(f"您已经进行了{count}次分析。是否感谢作者？")
        print("-------------------------------------------\n")
        choice = input("是否继续？按'Y'感谢, 其他键退出。")
        if choice.upper() not in ['Y', 'YES']:
            print("期待您的下次使用！")
            return 0
        else:
            line.p(50)
            print(' '*15 + '感谢您的认可!O(∩_∩)O')
            line.p(50)
            print()
            return 1
    elif count == -1:
        return 1
    else:
        print(f"{line.r(20)}\n\n{line.r(20)}")
        return 1


if __name__ == '__main__':
    a = 1
    count = -1
    while a:
        # 数据处理总函数
        data_analysis()
        input("按任意键继续...")
        count += 1
        # 感谢函数
        a = thanks()

        

