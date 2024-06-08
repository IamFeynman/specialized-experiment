import numpy as np
import sounddevice as sd
import time
import matplotlib.pyplot as plt#绘个图
#参数
fs = 44100 # 采样率，44100是CD等音频设备的常用采样率
length = 1 #时长s

t = np.arange(fs * length) #自然数列，相当于定义了n
'''
#DTMF的频率组合，
注意这是一个字典（dict）结构，即键值对（key-value）的集合，
键是个字符串，即拨号键，值是数组（方括号内）
'''
num = {
    '0': [941, 1336],
    '1': [697, 1209],
    '2': [697, 1336],
    '3': [697, 1477],
    '4': [770, 1209],
    '5': [770, 1336],
    '6': [770, 1477],
    '7': [852, 1209],
    '8': [852, 1336],
    '9': [852, 1477],
}

#函数：生成对应的sin和合并后的波形
def getNumWave(numstr):
    # num[numstr][0]，即DTMF的低频（Hz）
    # num[numstr][1]为高频值（Hz），
    #频率乘以2pi，得到模拟角频率(Angular frequency）
    # 需要计算数字角频率 = 模拟角频率 * 抽样间隔，抽烟间隔 = 1 / fs
    low_df = 2 * np.pi * num[numstr][0] / fs
    high_df = 2 * np.pi * num[numstr][1] / fs
    print(low_df,high_df)

    # 2pi *频率
    discrete_sin1 = np.sin(low_df * t)  #生成低频部分正弦波
    discrete_sin2 = np.sin(high_df * t)  # 生成高频部分正弦波
    DTMFsin = discrete_sin1 + discrete_sin2 #组合一下
    return discrete_sin1,discrete_sin2,DTMFsin


#播放
numstr = '0'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)

numstr = '1'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.figure()
len = 200 #折线图长度
plt.subplot(331)#画布位置1
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='purple')#波形合成之后的图
numstr = '2'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.subplot(332)#画布位置2
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='red')#波形合成之后的图
numstr = '3'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.subplot(333)#画布位置3
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='green')#波形合成之后的图
numstr = '4'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.subplot(334)#画布位置4
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='black')#波形合成之后的图
numstr = '5'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.subplot(335)#画布位置5
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='blue')#波形合成之后的图
numstr = '6'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.subplot(336)#画布位置6
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='m')#波形合成之后的图
numstr = '7'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.subplot(337)#画布位置7
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='c')#波形合成之后的图
numstr = '8'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.subplot(338)#画布位置8
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='y')#波形合成之后的图
numstr = '9'
sin1,sin2,DTMFsin = getNumWave(numstr)
sd.play(DTMFsin, fs)  # 播放
time.sleep(length)
plt.subplot(339)#画布位置9
plt.grid() #网格
plt.plot(t[:len*2],DTMFsin[:len*2],c='pink')#波形合成之后的图
plt.suptitle('DTMF LIST' )

plt.show()



# 2 * np.pi * f #就是模拟角频率Ω
# 1/fs就是Ts，Ts*Ω就是数字角频率w
# 此时的myarray就是n
# discrete_sin就是sin(nw)
#print('数组内容:',discrete_sin)
#sd.play(discrete_sin, fs) #播放
#time.sleep(2)