import pandas as pd
import gmplot

with open("./data.csv") as f:
    raw_data = pd.read_csv(
        "./cctvLocs.csv")
    lines = []

    for line in f:
        lines.append(line.rstrip('\n').split(','))
    for i in range(len(lines)):
        lines[i].pop()

    min_timeframe = 1000  # max timeframes
    for i in range(len(lines)):
        if len(lines[i]) < min_timeframe:
            min_timeframe = len(lines[i])

    for i in range(len(lines)):
        lines[i] = lines[i][0:min_timeframe]
    latitudes = raw_data["LAT"]
    longitudes = raw_data["LONG"]
    print(latitudes)
    print(longitudes)
    for i in range(min_timeframe):
        data = [[], [], []]
        for j in range(len(lines)):
            for _ in range(int(lines[j][i])):
                data[0].extend(latitudes[j*25:(j+1)*25])
                data[1].extend(longitudes[j*25:(j+1)*25])
        gmap = gmplot.GoogleMapPlotter(1.3608985, 103.8052229, 11)
        gmap.heatmap(data[0], data[1])
        gmap.draw(
            "./heatMapFiles/heatMap"+str(i)+".html")

