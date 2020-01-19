import matplotlib.pyplot as plt
import numpy as np
import csv


def plot_bar(numVehicles, time):
    objects = ('Cam1', 'Cam2', 'Cam3', 'Cam4')
    y_pos = np.arange(len(objects))

    plt.bar(y_pos, numVehicles, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of Vehicles')

    plt.title('Number of vehicles detected at each CCTV')

    plt.savefig('./Graphs/%d.png' % time)
    plt.close()


with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #fake = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)
    j = 0
    minRow = len(data[0])
    for row in data:
        if j==4: break
        j+=1
        row.pop()
        # print(len(row))
        if len(row) < minRow:
            minRow = len(row)
    # print(data)
    numVehicles = [0, 0, 0, 0]
    line_count = 0
    time = 0
    while time < minRow-1:
        line_count = 0
        for row in data:
            print("time %d" % time)
            if time >= len(row):
                numVehicles[line_count] = 0
            else:
                numVehicles[line_count] = eval(row[time])
            line_count += 1
            if line_count == 4:
                break
        time += 1
        plot_bar(numVehicles, time-1)
csv_file.close()
