#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import os
import sys

# -------------------- BANNER --------------------
def banner():
    os.system('clear')
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     ██████╗  █████╗ ███████╗███████╗██╗    ██╗         ║
    ║     ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║         ║
    ║     ██████╔╝███████║███████╗███████╗██║ █╗ ██║         ║
    ║     ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║         ║
    ║     ██║     ██║  ██║███████║███████║╚███╔███╔╝         ║
    ║     ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝          ║
    ║                                                          ║
    ║         🇮🇳 INDIAN PASSWORD GENERATOR 🇮🇳               ║
    ║                  BY RVG DEVELOPER                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)

# -------------------- INDIAN NAME & WORD LISTS --------------------
first_names = [
    "rahul", "raj", "amit", "vikram", "suresh", "mahesh", "ramesh", "ankit", "rohit", "mohit",
    "priya", "neha", "pooja", "ritu", "kavita", "anjali", "sonia", "mona", "tina", "sneha",
    "arjun", "karan", "deepak", "sunil", "anil", "pankaj", "ajay", "vijay", "sanjay", "naveen",
    "divya", "kiran", "jyoti", "arti", "shilpa", "rekha", "meena", "seema", "geeta", "sita",
    "vishal", "amit", "manish", "rahul", "rajesh", "vineet", "manoj", "ashok", "ravi", "gopal",
    "sarita", "komal", "nisha", "sapna", "radha", "sakshi", "kajal", "ayushi", "tanya", "aditi"
]

last_names = [
    "sharma", "verma", "singh", "kumar", "gupta", "joshi", "patel", "reddy", "rao", "nair",
    "menon", "iyer", "tripathi", "mishra", "saxena", "chopra", "malhotra", "khanna", "mehta", "sethi",
    "agrawal", "goyal", "jain", "khatri", "pandey", "tiwari", "dubey", "yadav", "choudhary", "rathore"
]

city_names = [
    "delhi", "mumbai", "bangalore", "chennai", "kolkata", "pune", "hyderabad", "ahmedabad", "jaipur", "lucknow",
    "noida", "gurgaon", "chandigarh", "bhopal", "indore", "nagpur", "surat", "vadodara", "amritsar", "agra"
]

birth_years = [str(y) for y in range(1970, 2010)]
special_chars = ["@", "#", "$", "!", "_", "-", "."]
common_numbers = ["123", "1234", "12345", "007", "786", "143", "000", "999", "101", "2020", "2021", "2022", "2023", "2024"]

# -------------------- GENERATE PASSWORDS --------------------
def generate_password():
    pattern = random.randint(1, 20)
    
    if pattern == 1:
        # name + year
        return random.choice(first_names) + random.choice(birth_years)
    elif pattern == 2:
        # name + year + special
        return random.choice(first_names) + random.choice(special_chars) + random.choice(birth_years)
    elif pattern == 3:
        # first + last + number
        return random.choice(first_names) + random.choice(last_names) + random.choice(common_numbers)
    elif pattern == 4:
        # first + city + year
        return random.choice(first_names) + random.choice(city_names) + random.choice(birth_years)
    elif pattern == 5:
        # first + special + city
        return random.choice(first_names) + random.choice(special_chars) + random.choice(city_names)
    elif pattern == 6:
        # name + city + number
        return random.choice(first_names) + random.choice(city_names) + random.choice(common_numbers)
    elif pattern == 7:
        # last + year + special
        return random.choice(last_names) + random.choice(birth_years) + random.choice(special_chars)
    elif pattern == 8:
        # pet name + number
        pet_names = ["tiger", "rocky", "tommy", "sheru", "chintu", "pinky", "lucky", "jack", "leo", "max", "simba", "brownie"]
        return random.choice(pet_names) + random.choice(common_numbers)
    elif pattern == 9:
        # name + birth year + special
        return random.choice(first_names) + random.choice(birth_years) + random.choice(special_chars)
    elif pattern == 10:
        # first + last + year
        return random.choice(first_names) + random.choice(last_names) + random.choice(birth_years)
    elif pattern == 11:
        # name + "123" + special
        return random.choice(first_names) + "123" + random.choice(special_chars)
    elif pattern == 12:
        # name + "786" + year
        return random.choice(first_names) + "786" + random.choice(birth_years)
    elif pattern == 13:
        # first + @ + last + number
        return random.choice(first_names) + "@" + random.choice(last_names) + random.choice(common_numbers)
    elif pattern == 14:
        # name + "2024"
        return random.choice(first_names) + "2024"
    elif pattern == 15:
        # name + "123456"
        return random.choice(first_names) + "123456"
    elif pattern == 16:
        # full name (first + last) + special
        return random.choice(first_names) + random.choice(last_names) + random.choice(special_chars)
    elif pattern == 17:
        # name + number + special
        return random.choice(first_names) + random.choice(common_numbers) + random.choice(special_chars)
    elif pattern == 18:
        # city + year + special
        return random.choice(city_names) + random.choice(birth_years) + random.choice(special_chars)
    elif pattern == 19:
        # name + "21" + special
        return random.choice(first_names) + "21" + random.choice(special_chars)
    elif pattern == 20:
        # first + last + city + number
        return random.choice(first_names) + random.choice(last_names) + random.choice(city_names) + random.choice(common_numbers)
    else:
        return random.choice(first_names) + random.choice(birth_years)

# -------------------- MAIN --------------------
def main():
    banner()
    
    print("\n" + "="*60)
    print("🇮🇳 INDIAN PASSWORD GENERATOR")
    print("="*60)
    print("📌 Passwords will be saved to: /sdcard/Download/password.txt")
    print("="*60 + "\n")
    
    while True:
        try:
            count_input = input("🔢 Enter number of passwords to generate (e.g., 5, 10, 100, 99999999): ").strip()
            if count_input.lower() == 'exit':
                print("👋 Exiting...")
                sys.exit(0)
            count = int(count_input)
            if count <= 0:
                print("❌ Please enter a positive number.\n")
                continue
            break
        except ValueError:
            print("❌ Invalid input! Please enter a number or type 'exit'.\n")
    
    # Generate passwords
    print(f"\n⏳ Generating {count:,} passwords...")
    
    passwords = set()
    while len(passwords) < count:
        passwords.add(generate_password())
        if len(passwords) % 1000 == 0:
            print(f"📊 Generated {len(passwords):,} passwords...")
    
    # Save to /sdcard/Download/
    download_dir = "/sdcard/Download"
    if not os.path.exists(download_dir):
        print("\n⚠️  /sdcard/Download/ not found!")
        print("📌 Running termux-setup-storage...")
        os.system("termux-setup-storage")
        print("📌 Please grant storage permission and restart the script.")
        sys.exit(1)
    
    filepath = os.path.join(download_dir, "password.txt")
    
    with open(filepath, 'w') as f:
        for pwd in passwords:
            f.write(pwd + "\n")
    
    print("\n" + "="*60)
    print("✅ " + "="*57)
    print(f"✅ Generated {len(passwords):,} passwords")
    print(f"📂 Saved to: {filepath}")
    print("📊 File size: {:.2f} MB".format(os.path.getsize(filepath) / (1024 * 1024)))
    print("✅ " + "="*57)
    print("="*60 + "\n")
    
    print("📌 You can now use this file for cracking:")
    print(f"   python cracker.py {filepath}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
        print("👋 Exiting...")
