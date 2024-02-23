import csv  # import the csv module

# Reading the csv as lists
filename = "sample.csv"
fields = []
rows = []
try:
    with open(filename, "r") as csvfile: # Open the file
        csvreader = csv.reader(csvfile) # Create CSV reader object
        fields = next(csvreader) # Read the first row from the iterator
        for row in csvreader: # Read remaining rows
            rows.append(row)
except Exception as error:
    print(error)

print(fields)
print(rows)


with open(filename, mode="r") as file:
    # Create a CSV reader with DictReader
    csv_reader = csv.DictReader(file)

    # Initialize an empty list to store the dictionaries
    data_list = []

    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Append each row (as a dictionary) to the list
        data_list.append(row)
    print(data_list)

""" Different types of sorts. """
list_of_tuples = [(1, "f"), (2, "a"), (3, "c")]
sorted_list = sorted(list_of_tuples, key=lambda x: x[1], reverse=True)
print(sorted_list)  # Output: [(2, 'a'), (3, 'c'), (1, 'f')]

# Sorting a list of integers in ascending order
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()
print(numbers)  # Output: [1, 1, 2, 3, 4, 5, 6, 9]

# Sorting in descending order
numbers.sort(reverse=True)
print(numbers)  # Output: [9, 6, 5, 4, 3, 2, 1, 1]
