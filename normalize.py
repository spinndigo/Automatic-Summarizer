# This file simply contains a function for normalizing a set of data


def normalize(data):    # A list of numbers
        i = 0

        for value in data:
            data[i] = (data[i] - min(data))/ (max(data) - min(data))
            i += 1

        return data


