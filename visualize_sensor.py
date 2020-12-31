import pandas as pd
import matplotlib.pyplot as plt
import os

path = r"Z:\2020-JG18-T31Bewegungsanalyse-Pelz-Kroener\05-Messfahrten_Daten\Sensor Datenrate"

def average_time(csv, pos):
    lists = []
    for i in range(1,len(csv)):
        a = (csv[pos][i] - csv[pos][i-1])
        lists.append(a/1000000)
    #print(len(lists))
    return(sum(lists)/len(lists)) # return in ms

def plots(csv, savepath):
    data = csv
    
    # ACC
    avg_time = average_time(csv, "Time_in_ns")
    print(avg_time)
    start, end = start_end(savepath, avg_time)
    
    time_acc = list(data["Time_in_ns"])
    begin = time_acc[start]
    for i in range(len(time_acc)):
        time_acc[i] = time_acc[i]-begin
    time_acc = time_acc[start:end]
    acc_x = list(data["ACC_X"])[start:end]
    acc_y = list(data["ACC_Y"])[start:end]
    acc_z = list(data["ACC_Z"])[start:end]

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
    fig.savefig(savepath + "acc.pdf", dpi=1200)

    #LINEAR_ACC
    avg_time = average_time(csv, "Time_in_ns.1")
    print(avg_time)
    start, end = start_end(savepath, avg_time)
    
    time_acc1 = list(data["Time_in_ns.1"])
    begin = time_acc1[0]
    for i in range(len(time_acc1)):
        time_acc1[i] = time_acc1[i]-begin
    time_acc1 = time_acc1[start:end]
    linear_acc_x = list(data["LINEAR_ACC_X"])[start:end]
    linear_acc_y = list(data["LINEAR_ACC_Y"])[start:end]
    linear_acc_z = list(data["LINEAR_ACC_Z"])[start:end]

    # plot
    fig, axs = plt.subplots(3)
    fig.suptitle('Sensordaten')
    axs[0].plot(time_acc1, linear_acc_x)
    axs[1].plot(time_acc1, linear_acc_y)
    axs[2].plot(time_acc1, linear_acc_z)

    axs[0].set(xlabel='Zeit', ylabel='LINEAR_ACC_X')
    axs[1].set(xlabel='Zeit', ylabel='LINEAR_ACC_Y')
    axs[2].set(xlabel='Zeit', ylabel='LINEAR_ACC_Z')

    plt.subplots_adjust(bottom = 0.06, top = 0.9)
    fig.savefig(savepath + "linear_acc.pdf", dpi=1200)

    # W
    avg_time = average_time(csv, "Time_in_ns.2")
    print(avg_time)
    start, end = start_end(savepath, avg_time)
    
    time_acc2 = list(data["Time_in_ns.2"])
    begin = time_acc2[0]
    for i in range(len(time_acc2)):
        time_acc2[i] = time_acc2[i]-begin
    time_acc2 = time_acc2[start:end]
    w_X = list(data["w_X"])[start:end]
    w_Y = list(data["w_Y"])[start:end]
    w_Z = list(data["w_Z"])[start:end]

    # plot
    fig, axs = plt.subplots(3)
    fig.suptitle('Sensordaten')
    axs[0].plot(time_acc2, w_X)
    axs[1].plot(time_acc2, w_Y)
    axs[2].plot(time_acc2, w_Z)

    axs[0].set(xlabel='Zeit', ylabel='W_X')
    axs[1].set(xlabel='Zeit', ylabel='W_Y')
    axs[2].set(xlabel='Zeit', ylabel='W_Z')

    plt.subplots_adjust(bottom = 0.06, top = 0.9)
    fig.savefig(savepath + "w.pdf", dpi=1200)

def start_end(csvpath, avg_time):
    print(csvpath)
    avg_time = avg_time / 1000
    avg_time = 1 / avg_time
    if "100_Hz" in csvpath:
        start = avg_time*15
        end = avg_time*25
        print("Anfallende Daten pro Minute: 6000")
    elif "50_Hz" in csvpath:
        start = avg_time*15
        end = avg_time*25
        print("Anfallende Daten pro Minute: 3000")
    elif "20_Hz" in csvpath:
        start = avg_time*15
        end = avg_time*25
        print("Anfallende Daten pro Minute: 1200")
    elif "10_Hz" in csvpath:
        start = avg_time*15
        end = avg_time*25
        print("Anfallende Daten pro Minute: 600")
    else:
        print("INVALID PATH")
    return(int(start), int(end))

if __name__ == "__MAIN__":
    for folder in os.listdir(path):
        csvpath = path + "/" + folder
        for csvdata in os.listdir(csvpath):
            if "GPS" in (csvpath+"/"+csvdata):
                None
            else:
                csv = pd.read_csv(csvpath+"/"+csvdata, sep = ",")
                if("V1" in csvdata):
                    print("-----------")
                    # print(csvpath+"/"+csvdata)
                    # print((csv["Time_in_ns"][len(csv)-1] - csv["Time_in_ns"][0])/1000000)
                    # print(average_time(csv))
                    # avg_time = average_time(csv)
                    plots(csv, csvpath)
                    print("-----------")