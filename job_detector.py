def check_job_posting(company, fee_required, has_website, stipend, description_length):
    """
    Checks one job posting for common scam red flags.
    Returns a risk level ('LOW', 'MEDIUM', 'HIGH') and the list of specific problems found.
    """
    red_flags = []
    
    if fee_required:
        red_flags.append("Asks for upfront payment")
    
    if not has_website:
        red_flags.append("No verifiable company website")
    
    if stipend < 5000:
        red_flags.append("Unusually low stipend")
    
    if description_length < 100:
        red_flags.append("Suspiciously short/vague job description")
    
    if len(red_flags) == 0:
        risk = "LOW"
    elif len(red_flags) <= 2:
        risk = "MEDIUM"
    else:
        risk = "HIGH"
    
    return risk, red_flagsdef analyze_all_postings(filename):
    """
    Reads a CSV file of job postings and checks each one.
    Prints a full report.
    """
    with open(filename, "r") as file:
        lines = file.readlines()
    
    # First line is the header, skip it
    data_lines = lines[1:]
    
    print("=" * 50)
    print("JOB POSTING SCAM ANALYSIS REPORT")
    print("=" * 50)
    
    for line in data_lines:
        line = line.strip()
        parts = line.split(",")
        
        company = parts[0]
        fee_required = parts[1] == "True"
        has_website = parts[2] == "True"
        stipend = int(parts[3])
        description_length = int(parts[4])
        
        risk, flags = check_job_posting(company, fee_required, has_website, stipend, description_length)
        
        print(f"\nCompany: {company}")
        print(f"Risk Level: {risk}")
        if flags:
            print("Red Flags Found:")
            for flag in flags:
                print(f"  - {flag}")
        else:
            print("No red flags found - looks legitimate")
