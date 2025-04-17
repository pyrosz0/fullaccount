import sqlite3
import os

def create_database():

    # Define the database name
    DATABASE_NAME = 'fullaccount.db'  

    # Delete the database file if it exists
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)


    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(DATABASE_NAME)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create the categories table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        keywords TEXT 
    )
    ''')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        accounttype TEXT NOT NULL,
        accountnumber TEXT NOT NULL,
        date INTEGER NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        merchant TEXT NOT NULL,
        category TEXT NOL NULL
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()

    transaction_categories = [
        {
            "category": "groceries",
            "search_terms": [
                "walmart", "costco", "kroger", "safeway", "aldi", "whole foods",
                "trader joes", "publix", "meijer", "dollarama", "freshco",
                "bulk barn", "sobeys", "zehrs", "foodland", "food basics", "iga",
                "the great canadian bagel", "superstore", "no frills", "save on foods",
                "piggly wiggly", "h-e-b", "giant eagle", "food lion", "winco foods",
                "market basket", "shoprite", "stater bros", "ralphs", "vons", "grocery"
            ]
        },
        {
            "category": "restaurants",
            "search_terms": [
                "mcdonalds", "starbucks", "chipotle", "olive garden", "panda express",
                "dominos", "subway", "taco bell", "panera bread", "cheesecake factory",
                "a&w", "bâton rouge", "beavertails", "big smoke burger", "booster juice",
                "cactus club cafe", "fish & chips", "chairmans brands", "chez ashton",
                "coffee time", "cora breakfast & lunch", "crabby joes", "country style",
                "la diperie", "dixie lee", "druxys", "dunns", "earls", "east side marios",
                "edo japan", "eggspectation", "eggsquis", "freshii", "grinners food systems limited",
                "harveys", "hero certified burgers", "imvescor restaurants inc", "jack astors bar and grill",
                "jimmy the greek", "joey", "joeys seafood restaurants", "the keg",
                "kelseys original roadhouse", "king of donair", "kinton ramen",
                "la belle province", "lafleur restaurants", "lone star texas grill",
                "mary browns", "mandarin restaurant", "mikes", "milestones grill and bar",
                "montanas cookhouse", "moxies", "new york fries", "nickels grill & bar",
                "normandin", "nuburger", "the old spaghetti factory", "opa! of greece",
                "osmows shawarma", "panago", "the pickle barrel", "pür & simple",
                "recipe unlimited", "royal paan", "richtree market", "shoeless joes",
                "smokes poutinerie", "st. louis bar and grill", "st-hubert", "second cup",
                "smittys family restaurants", "sunset grill", "swiss chalet", "symphony cafe",
                "thaï express", "tim hortons", "wild wing", "wimpys diner", "wendys", "kfc",
                "dairy queen", "arbys", "chick-fil-a", "five guys", "shake shack",
                "pizzeria uno", "red lobster", "outback steakhouse", "buffalo wild wings",
                "cracker barrel", "dennys", "ihop", "tgi fridays", "applebees", "restaurant", "pizza"
            ]
        },
        {
            "category": "gas",
            "search_terms": [
                "esso", "petro canada", "husky", "ultramar", "exxon", "chevron",
                "shell", "bp", "mobil", "sunoco", "76", "circle k", "valero",
                "racetrac", "quicktrip", "marathon", "convenience store", "gas station", "fuel"
            ]
        },
        {
            "category": "maintenance",
            "search_terms": [
                "home depot", "home hardware", "lowes", "rona", "princess auto", "canadian tire",
                "ace hardware", "menards", "true value", "harbor freight", "lumber yard",
                "plumbing supply", "electrical supply", "paint store", "tool rental"
            ]
        },
        {
            "category": "travel",
            "search_terms": [
                "travel", "travels", "airline", "hotel", "motel", "hostel", "car rental",
                "expedia", "booking.com", "airbnb", "travelocity", "tripadvisor",
                "southwest airlines", "delta", "united", "american airlines", "jetblue",
                "hertz", "avis", "enterprise", "marriott", "hilton", "holiday inn"
            ]
        },
        {
            "category": "entertainment",
            "search_terms": [
                "entertainment", "movies", "spotify", "netflix", "hulu", "disney", "hbo",
                "hulu max", "hulu+", "concert", "theater", "live show", "amc theaters",
                "fandango", "ticketmaster", "broadway", "comedy club", "arcade",
                "video games", "streaming service", "cable subscription", "pay-per-view"
            ]
        },
        {
            "category": "clothing",
            "search_terms": [
                "clothing", "clothes", "rickis", "winners", "lululemon", "h&m", "urban planet",
                "gap", "old navy", "forever 21", "zara", "express", "banana republic",
                "anthropologie", "j crew", "macys", "nordstrom", "tj maxx", "ross",
                "adidas", "nike", "puma", "under armour", "the north face"
            ]
        },
        {
            "category": "utilities",
            "search_terms": [
                "utilities", "utility", "enbridge", "electricity", "water", "gas",
                "internet", "cable", "phone", "sewer", "trash", "recycling", "landline",
                "cell phone", "satellite", "energy provider", "municipal services"
            ]
        },
        {
            "category": "internet and cell phones",
            "search_terms": [
                "rogers", "bell", "public mobile", "centurylink", "sprint", "verizon",
                "at&t", "t-mobile", "comcast", "xfinity", "spectrum", "charter",
                "mobile plan", "data plan", "internet service", "cellular service"
            ]
        },
        {
            "category": "personal care",
            "search_terms": [
                "nails", "facial", "makeup", "beauty", "beauties", "hair salon",
                "barber shop", "spa", "massage", "skincare", "cosmetics", "fragrance",
                "personal hygiene", "wellness", "fitness", "gym membership"
            ]
        },
        {
            "category": "rent",
            "search_terms": [
                "rent", "rents", "apartment", "lease", "landlord", "tenant", "rent payment",
                "rental agreement", "property management", "housing", "real estate"
            ]
        },
        {
            "category": "insurance",
            "search_terms": [
                "insurance", "insurances", "health insurance", "auto insurance",
                "home insurance", "life insurance", "renters insurance", "liability insurance",
                "travel insurance", "disability insurance", "insurance premium"
            ]
        },
        {
            "category": "healthcare",
            "search_terms": [
                "healthcare", "health", "doctor", "hospital", "clinic",
                "urgent care", "pharmacy", "medication", "wellness", "physical therapy",
                "dentist", "optometrist", "chiropractor", "psychologist", "therapist"
            ]
        },
        {
            "category": "education",
            "search_terms": [
                "education", "educational", "tuition", "school", "college", "university",
                "online courses", "textbooks", "student loans", "scholarship", "training",
                "workshop", "seminar", "certification", "continuing education"
            ]
        },
        {
            "category": "amazon",
            "search_terms": [
                "amzn", "amazon", "prime", "kindle", "aws", "amazon fresh", "audible",
                "amazon music", "amazon video", "amazon web services"
            ]
        },
        {
            "category": "transfer",
            "search_terms": [
                "transfer", "etransfer", "wire transfer", "money transfer", "paypal",
                "venmo", "zelle", "cash app", "remittance", "bank transfer"
            ]
        },
        {
            "category": "taxes",
            "search_terms": [
                "taxes", "tax return", "tax preparation", "irs", "tax refund", "tax filing",
                "state taxes", "federal taxes", "property taxes", "sales tax"
            ]
        },
        {
            "category": "income",
            "search_terms": [
                "income", "deposit", "payroll", "salary", "wages", "commission", "bonus",
                "interest", "dividends", "rental income", "freelance income"
            ]
        },
        {
            "category": "vehicles",
            "search_terms": [
                "vehicles", "ideal supply", "car quest", "napa", "auto zone", "car repair",
                "oil change", "tire shop", "auto parts", "vehicle registration", "insurance",
                "maintenance", "car wash", "detailing"
            ]
        },
        {
            "category": "payments",
            "search_terms": [
                "payment", "payments", "mastercard", "visa", "credit card", "debit card",
                "cash", "check", "payment plan", "installment", "transaction fee"
            ]
        },
        {
            "category": "equestrian",
            "search_terms": [
                "bahr", "greenhawk", "bakers saddlery", "doonaree", "horse feed",
                "stable", "equestrian", "riding lessons", "horse trailer", "farrier"
            ]
        },
        {
            "category": "mortgage",
            "search_terms": [
                "mortgage", "home loan", "refinance", "interest rate", "loan officer",
                "mortgage broker", "down payment", "escrow", "amortization", "closing costs"
            ]
        },
        {
            "category": "gifts",
            "search_terms": [
                "gifts", "gift card", "present", "birthday gift", "holiday gift",
                "anniversary gift", "wedding gift", "baby shower gift", "graduation gift"
            ]
        },
        {
            "category": "charity",
            "search_terms": [
                "charity", "donation", "nonprofit", "fundraiser", "philanthropy",
                "volunteer", "community service", "humanitarian", "social cause"
            ]
        },
        {
            "category": "pets",
            "search_terms": [
                "pets", "pet food", "pet supplies", "vet", "animal hospital",
                "grooming", "boarding", "pet insurance", "dog walker", "pet sitter"
            ]
        },
        {
            "category": "sports",
            "search_terms": [
                "sports", "gym", "fitness", "workout", "exercise", "yoga", "pilates",
                "crossfit", "personal trainer", "sports equipment", "athletic gear"
            ]
        },
        {
            "category": "home improvement",
            "search_terms": [
                "home improvement", "renovation", "remodeling", "construction", "landscaping",
                "interior design", "exterior design", "home decor", "furniture", "appliances"
            ]
        },
        {
            "category": "office supplies",
            "search_terms": [
                "office supplies", "stationery", "printer ink", "paper", "envelopes",
                "folders", "binders", "desk accessories", "office furniture"
            ]
        },
        {
            "category": "loans",
            "search_terms": [
                "loan", "loans", "personal loan", "student loan", "auto loan",
                "home equity loan", "payday loan", "credit union", "lender", "interest rate"
            ]
        },
        {
            "category": "uncategorized",
            "search_terms": []
        }
    ]

    for category_data in transaction_categories:
        category_name = category_data["category"]
        keywords = ", ".join(category_data["search_terms"])  # Convert list to comma-separated string
        cursor.execute("""
        INSERT INTO categories (name, keywords)
        VALUES (?, ?)
        """, (category_name, keywords))

    # Commit the transaction
    conn.commit()


    conn.close()

    return True
