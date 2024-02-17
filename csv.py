def read_csv():
    filepath = "data/ItemsCF.csv"
    file = open(filepath)

    # List of lists defining main ingredient and Carbon Footprint
        # [0] = main ingredient
        # [1] = CF
    item_CF = []

    for line in file:
        line = line.strip().split(",")
        item = line[3]
        cf = line[5]
        item_CF.append([item, cf])

    print(item_CF)
    return item_CF

if __name__ == '__main__':
    read_csv()