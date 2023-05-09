import csv
import matplotlib.pyplot as plt

def plot_norway(special_lat,special_long,filename_save):
    with open("NO.txt", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter = "\t")

        next(reader)  

        long,lat = [], []

        for row in reader:
            long.append(float(row[4]))
            lat.append(float(row[5]))

        plt.scatter(lat,long,linewidths=0.1)
        plt.scatter(special_lat,special_long,linewidths=3,c="m")
        plt.savefig(f"map_images/{filename_save}")
        # plt.show()


if __name__ == "__main__":
    plot_norway([12,10],[60,70],"test.png")



