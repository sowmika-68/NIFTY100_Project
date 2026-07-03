import csv

output_file = "output/capital_allocation.csv"

header = [
    "company_id",
    "year",
    "cfo_sign",
    "cfi_sign",
    "cff_sign",
    "pattern_label",
]

sample_data = [
    [1, 2024, "+", "-", "-", "Reinvestor"],
    [2, 2024, "+", "-", "-", "Shareholder Returns"],
    [3, 2024, "-", "+", "+", "Distress Signal"],
]

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(header)

    writer.writerows(sample_data)

print(f"{output_file} created successfully.")
