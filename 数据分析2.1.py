
print("正在载入请稍等……")

import importlib
import subprocess

required_libraries = ['numpy', 'decimal', 'scipy']

def is_library_installed(library_name):
    try:
        importlib.import_module(library_name)
        return True
    except ImportError:
        return False

if not is_library_installed('tqdm'):
    print("tqdm未安装，正在尝试使用pip安装...")
    command = 'pip install tqdm'
    subprocess.call(command, shell=True)

from tqdm import tqdm

missing_libraries = []
for library in required_libraries:
    if not is_library_installed(library):
        missing_libraries.append(library)

if missing_libraries:
    for library in tqdm(missing_libraries, desc='Installing Libraries'):
        print(f'\n{library}库没有安装，正在尝试使用pip安装...')
        command = f'pip install -i https://pypi.tuna.tsinghua.edu.cn/simple {library}'
        subprocess.call(command, shell=True)
    print("依赖库已经全部安装完成。")
else:
    print("依赖库已经全部安装好。")

print("程序即将开始执行...")



import signal
import sys
import numpy as np
from decimal import Decimal as D
from scipy.stats import t
import functools

nums = []  # 创建全局变量


def line(length):
    print('-' * length)


def signal_handler(signal, frame):
    # 屏幕提示的文本可以根据个人兴趣设置
    print("\n（检测到中断，输入已保存，按“e”键终止程序，回车后开始分析）", end="")
    # 清空数据并等待下一轮输入
    global nums
    #nums.clear()
    while True:
        try:
            choice = input()
            if choice.lower() == "e":
                sys.exit(0)
            else:
                break
        except KeyboardInterrupt:
            continue


def data_analysis():
    global nums
    nums = []
    sum_nums = 0
    sum_squares = 0

    # data_analysis() 中注册信号处理方法
    signal.signal(signal.SIGINT, functools.partial(signal_handler))

    while True:
        try:
            data = input("请输入数据 (按回车键结束): ")
            if not data:
                break

            try:
                num = D(data)
            except:
                print(f'“{data}”不是数字吧，再看一眼？')
                continue

            nums.append(num)
            sum_nums += num
            sum_squares += num ** 2

        except KeyboardInterrupt:
            signal_handler(None, None)  # 将参数修改为 (None, None)

    n = len(nums)
    if n == 0:
        print("喂喂喂，你没输入数据！")
        return
    elif n == 1:
        print("一个数字可不能拿来分析，再整几个来")
        return

    mean = sum_nums / D(n)
    abs_deviations = np.abs(np.array(nums) - mean)
    avg_abs_deviation = np.mean(abs_deviations)
    rel_std_dev, variance, std_dev = None, None, None
    if mean == 0:
        rel_avg_abs_deviation = 0 if avg_abs_deviation == 0 else float("inf")
    else:
        rel_avg_abs_deviation = avg_abs_deviation / mean * 100
    print("-" * 20)
    print(f"平均数：       {mean:.4f}")
    print(f"绝对偏差di：   {[f'{d:.4f}' for d in abs_deviations]}")
    print(f"平均偏差：     {avg_abs_deviation:.4f}")
    print(f"相对平均偏差： {rel_avg_abs_deviation:.4f} %")
    if sum_nums == 0:
        print("标准偏差：     和为0，无法计算")
        print("相对标 准偏差： 和为0，无法计算")
        print("方差：         和为0，无法计算")
    else:
        rel_std_dev = np.std(nums, ddof=1) / mean
        variance = (sum_squares - sum_nums ** 2 / D(n)) / (n - 1)
        std_dev = np.std(nums, ddof=1)
        print(f"标准偏差：     {std_dev:.4f}")
        print(f"相对标准偏差： {rel_std_dev:.4f} %")
        print(f"方差：         {variance:.4f}")

    while True:
        if sum_nums == 0:
            print("置信区间：     和为0，无法计算")
            break

        try:
            conf_level = input('\n请输入置信度 (0-100)，或按回车键跳过：')
            if conf_level == '':
                break
            conf_level = float(conf_level)
        except ValueError:
            print("再看一眼，你输入的好像确实不是数字")
            continue

        if not (0 < conf_level < 100):
            print("置信区间诶老哥，麻烦输入0到100之间的数")
            continue

        t_value = t.ppf((conf_level/100 + 1)/2, n-1)
        lower_ci = mean - D(t_value) * std_dev / D(n).sqrt()
        upper_ci = mean + D(t_value) * std_dev / D(n).sqrt()
        print(f"{conf_level}% 置信区间：[{lower_ci:.4f}, {upper_ci:.4f}]")
        break

    line(20)
    return


if __name__ == '__main__':
    count = 0
    while True:
        data_analysis()
        input("按任意键继续...")
        count += 1
        if count == 3 or (count > 0 and count % 5 == 0):
            print("\n-------------------------------------------")
            print(f"您已经进行了{count}次分析。是否感谢作者？")
            print("-------------------------------------------\n")
            choice = input("是否继续？按'Y'感谢，其他键退出。")
            if choice.upper() not in ['Y', 'YES']:
                print("期待您的下次使用！")
                break
            else:
                line(50)
                print(' '*15 + '感谢您的支持！O(∩_∩)O')
                line(50)
                print()
        else:
            print('-' * 20 + '\n\n' + '-' * 20)

