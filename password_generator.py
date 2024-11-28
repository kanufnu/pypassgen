#Program to auto generate passwords in python
import string
import secrets
import random
import urllib.request
import re


#common_password = set(['password', '123456', '123456789', 'qwerty', 'abc123', 'password1', 'letmein', 'welcome', '12345', 'password123'])
common_password = []
with open("common_word_list.txt","r") as commonpasswordfile:
    common_password = [_.strip() for _ in commonpasswordfile.readlines()]
print(common_password)
    
    

def is_common_password(password):
    
    return password.lower() in common_password

def generate_random_password(length, use_uppercase, use_numbers, use_symbols):
    
    
    char_set = string.ascii_lowercase  
    
    if use_uppercase:
        char_set += string.ascii_uppercase
    if use_numbers:
        char_set += string.digits
    if use_symbols:
        char_set += string.punctuation
    
    password = []
    
    
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_numbers:
        password.append(secrets.choice(string.digits))
    if use_symbols:
        password.append(secrets.choice(string.punctuation))
    
    
    password += [secrets.choice(char_set) for _ in range(length - len(password))]
    
    
    random.shuffle(password)

    return ''.join(password)


def generate_passphrase(word_count=4):
    
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
    response = urllib.request.urlopen(url)
    word_list = [word.decode('utf-8').strip() for word in response.readlines()]
    passphrase = ' '.join(secrets.choice(word_list) for _ in range(word_count))
    return passphrase

def check_strength(password):
    
    length_score = len(password) >= 12
    upper_score = any(c.isupper() for c in password)
    lower_score = any(c.islower() for c in password)
    digit_score = any(c.isdigit() for c in password)
    symbol_score = any(c in string.punctuation for c in password)
    
    pattern_check =bool(re.search(r'(abc|123|qwerty|password)', password, re.IGNORECASE))
    
    if pattern_check:
        return "Weak (contains common patterns)"
    
    if length_score and upper_score and lower_score and digit_score and symbol_score:
        return "Strong"
    elif length_score and (upper_score or lower_score or digit_score or symbol_score):
        return "Moderate"
    else:
        return "Weak"

def get_user_input():
    while True:
        try:
            length = int(input("Enter the password length (minimum 8, maximum 20): "))
            if length < 8 or length > 20:
                print("Password length should be between 8 and 20 characters.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")
        
    
    use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_numbers = input("Include numbers? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
    use_passphrase = input("Generate a passphrase instead of password? (y/n): ").lower() == 'y'
    
    return length, use_uppercase, use_numbers, use_symbols, use_passphrase

def generate_password(length, use_uppercase, use_numbers, use_symbols, use_passphrase):
    
    if use_passphrase:
        password = generate_passphrase(length // 5)   
    else:
        password = generate_random_password(length, use_uppercase, use_numbers, use_symbols)
    
   
    if not use_passphrase and is_common_password(password):
        print("Generated password is too common, regenerating...")
        password = generate_random_password(length, use_uppercase, use_numbers, use_symbols)
    
    return password

if __name__ == "__main__":

    length, use_uppercase, use_numbers, use_symbols, use_passphrase = get_user_input()

    
    password = generate_password(length, use_uppercase, use_numbers, use_symbols, use_passphrase) 

    
    strength = check_strength(password)
    
   
    print(f"Generated Password: {password}")
    print(f"Password Strength: {strength}")
