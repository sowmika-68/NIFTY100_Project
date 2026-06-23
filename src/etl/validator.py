import pandas as pd

companies = pd.read_excel(
    "data/companies.xlsx",
    header=1
)

print("Validator started")
print(companies.shape)
print(companies.columns)

import pandas as pd

# Load Companies Dataset
companies = pd.read_excel(
    "data/companies.xlsx",
    header=1
)

print("Validator Started")
print("Rows:", len(companies))

# DQ-01 Primary Key Uniqueness
duplicate_ids = companies[companies["id"].duplicated()]

if len(duplicate_ids) == 0:
    print("✅ DQ-01 Passed: No Duplicate IDs Found")
else:
    print("❌ DQ-01 Failed")
    print(duplicate_ids)

import pandas as pd

validation_failures = []

companies = pd.read_excel(
    "data/companies.xlsx",
    header=1
)

duplicate_ids = companies[
    companies["id"].duplicated()
]

if len(duplicate_ids) == 0:
    print("✅ DQ-01 Passed")
else:
    for value in duplicate_ids["id"]:
        validation_failures.append([
            "DQ-01",
            "CRITICAL",
            "Duplicate ID",
            value
        ])

print("Failures:", len(validation_failures))

missing_names = companies[
    companies["company_name"].isnull()
]

if len(missing_names) == 0:
    print("✅ DQ-02 Passed")
else:
    for row in missing_names.index:
        validation_failures.append([
            "DQ-02",
            "CRITICAL",
            "Missing Company Name",
            row
        ])

missing_names = companies[
    companies["company_name"].isnull()
]

if len(missing_names) == 0:
    print("✅ DQ-02 Passed: No Missing Company Names")
else:
    print("❌ DQ-02 Failed")

    for row in missing_names.index:
        validation_failures.append([
            "DQ-02",
            "CRITICAL",
            "Missing Company Name",
            row
        ])

missing_website = companies[
    companies["website"].isnull()
]

if len(missing_website) == 0:
    print("✅ DQ-03 Passed: No Missing Website")
else:
    print("❌ DQ-03 Failed")

    for row in missing_website.index:
        validation_failures.append([
            "DQ-03",
            "WARNING",
            "Missing Website",
            row
        ])
print("\nMissing Websites:")
print(missing_website[["company_name", "website"]])

invalid_face = companies[
    companies["face_value"] <= 0
]

if len(invalid_face) == 0:
    print("✅ DQ-04 Passed")
else:
    print("❌ DQ-04 Failed")

    for value in invalid_face["face_value"]:
        validation_failures.append([
            "DQ-04",
            "CRITICAL",
            "Invalid Face Value",
            value
        ])

invalid_book = companies[
    companies["book_value"] <= 0
]

if len(invalid_book) == 0:
    print("✅ DQ-05 Passed")
else:
    print("❌ DQ-05 Failed")

    for value in invalid_book["book_value"]:
        validation_failures.append([
            "DQ-05",
            "CRITICAL",
            "Invalid Book Value",
            value
        ])

failure_df = pd.DataFrame(
    validation_failures,
    columns=[
        "rule_id",
        "severity",
        "issue",
        "value"
    ]
)

failure_df.to_csv(
    "output/validation_failures.csv",
    index=False
)

print("Total Failures:", len(validation_failures))

invalid_roe = companies[
    companies["roe_percentage"].isnull()
]

if len(invalid_roe) == 0:
    print("✅ DQ-06 Passed")
else:
    print("❌ DQ-06 Failed")

    for value in invalid_roe["roe_percentage"]:
        validation_failures.append([
            "DQ-06",
            "WARNING",
            "Invalid ROE Percentage",
            value
        ])
print("\nInvalid ROE Values:")
print(invalid_roe[["company_name", "roe_percentage"]])

for website in companies["website"]:

    if pd.notna(website):

        if not str(website).startswith(("http://", "https://")):

            validation_failures.append([
                "DQ-07",
                "WARNING",
                "Invalid URL",
                website
            ])

missing_nse = companies[
    companies["nse_profile"].isnull()
]

for row in missing_nse.index:
    validation_failures.append([
        "DQ-08",
        "WARNING",
        "Missing NSE Profile",
        row
    ])

missing_bse = companies[
    companies["bse_profile"].isnull()
]

for row in missing_bse.index:
    validation_failures.append([
        "DQ-09",
        "WARNING",
        "Missing BSE Profile",
        row
    ])

print("Total Failures:", len(validation_failures))

failure_df = pd.DataFrame(
    validation_failures,
    columns=[
        "rule_id",
        "severity",
        "issue",
        "value"
    ]
)

failure_df.to_csv(
    "output/validation_failures.csv",
    index=False
)

print("\nValidation Complete")
print("Total Failures:", len(validation_failures))