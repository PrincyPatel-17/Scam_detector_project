import csv

FEE_WORDS = ["registration fee", "security deposit", "processing fee",
             "pay a fee", "training fee", "refundable deposit", "wire transfer"]

def check_job_posting(row):
    red_flags = []

    if row["company_profile"].strip() == "":
        red_flags.append("No company information")

    if row["has_company_logo"] == "0":
        red_flags.append("No company logo")

    if row["salary_range"].strip() == "":
        red_flags.append("No salary listed")

    if len(row["description"]) < 300:
        red_flags.append("Very short description")

    text = row["description"].lower()
    for word in FEE_WORDS:
        if word in text:
            red_flags.append(f"Mentions fee: '{word}'")
            break

    if len(red_flags) <= 1:
        risk = "LOW"
    elif len(red_flags) <= 3:
        risk = "MEDIUM"
    else:
        risk = "HIGH"
    return risk, red_flags


def analyze_all_postings(filename):
    total = 0
    caught = 0
    real_fakes = 0

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total += 1
            risk, flags = check_job_posting(row)
            is_fake = row["fraudulent"] == "1"
            if is_fake:
                real_fakes += 1
                if risk in ("MEDIUM", "HIGH"):
                    caught += 1
            if total <= 10:
                print(f"\n{row['title']} | Risk: {risk} | Actually fake: {is_fake}")
                for flag in flags:
                    print(f"  - {flag}")

    print("\n" + "=" * 50)
    print(f"Postings checked: {total}")
    print(f"Actually fraudulent: {real_fakes}")
    print(f"Fraudulent ones my tool flagged: {caught}")
    print(f"Catch rate: {caught / real_fakes * 100:.1f}%")

analyze_all_postings("fake_job_postings.csv")
