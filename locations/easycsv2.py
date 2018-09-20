import io
import csv


def load(filename):
    with io.open(filename, "rt", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)


def write(data, filename):
    with io.open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
