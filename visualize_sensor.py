import pandas as pd
import matplotlib.pyplot as plt

start = 999
ende = 1999

path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/1609176039297_Foot_Walking_SENSOR.csv"
savepath = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/Sensor/"
data = pd.read_csv(path, sep = ",")

#ACC
time_acc = list(data["Time_in_ns"])

for i in range(1,len(time_acc)):
    if time_acc[i] < time_acc[i-1]:
        print("lukas hat verkackt")
        print(i)



begin = time_acc[start]
for i in range(len(time_acc)):
    time_acc[i] = time_acc[i]-begin
time_acc = time_acc[start:ende]
acc_x = list(data["ACC_X"])[start:ende]
acc_y = list(data["ACC_Y"])[start:ende]
acc_z = list(data["ACC_Z"])[start:ende]


#plot
fig, axs = plt.subplots(3)
fig.suptitle('Sensordaten')
axs[0].plot(time_acc, acc_x)
axs[1].plot(time_acc, acc_y)
axs[2].plot(time_acc, acc_z)

axs[0].set(xlabel='Zeit', ylabel='ACC_X')
axs[1].set(xlabel='Zeit', ylabel='ACC_Y')
axs[2].set(xlabel='Zeit', ylabel='ACC_Z')

plt.subplots_adjust(bottom = 0.06, top = 0.9)

fig.savefig(savepath + "acc.png")



#LINEAR_ACC
time_acc1 = list(data["Time_in_ns.1"])
begin = time_acc1[0]
for i in range(len(time_acc1)):
    time_acc1[i] = time_acc1[i]-begin
time_acc1 = time_acc1[start:ende]
linear_acc_x = list(data["LINEAR_ACC_X"])[start:ende]
linear_acc_y = list(data["LINEAR_ACC_Y"])[start:ende]
linear_acc_z = list(data["LINEAR_ACC_Z"])[start:ende]

#plot
fig, axs = plt.subplots(3)
fig.suptitle('Sensordaten')
axs[0].plot(time_acc1, linear_acc_x)
axs[1].plot(time_acc1, linear_acc_y)
axs[2].plot(time_acc1, linear_acc_z)

axs[0].set(xlabel='Zeit', ylabel='LINEAR_ACC_X')
axs[1].set(xlabel='Zeit', ylabel='LINEAR_ACC_Y')
axs[2].set(xlabel='Zeit', ylabel='LINEAR_ACC_Z')

plt.subplots_adjust(bottom = 0.06, top = 0.9)

fig.savefig(savepath + "linear_acc.png")



#W
time_acc2 = list(data["Time_in_ns.2"])
begin = time_acc2[0]
for i in range(len(time_acc2)):
    time_acc2[i] = time_acc2[i]-begin
time_acc2 = time_acc2[start:ende]
w_X = list(data["w_X"])[start:ende]
w_Y = list(data["w_Y"])[start:ende]
w_Z = list(data["w_Z"])[start:ende]

#plot
fig, axs = plt.subplots(3)
fig.suptitle('Sensordaten')
axs[0].plot(time_acc2, w_X)
axs[1].plot(time_acc2, w_Y)
axs[2].plot(time_acc2, w_Z)

axs[0].set(xlabel='Zeit', ylabel='W_X')
axs[1].set(xlabel='Zeit', ylabel='W_Y')
axs[2].set(xlabel='Zeit', ylabel='W_Z')

plt.subplots_adjust(bottom = 0.06, top = 0.9)

fig.savefig(savepath + "w.png")

print(time_acc[2742:2750])
print(time_acc1[2742:2750])
print(time_acc2[2742:2750])