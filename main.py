import requests, sys, os, time, re

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def logo():
    clear()
    print("\n")
    print("██████╗░██████╗░░█████╗░███████╗██╗░░██╗███████╗███╗░░██╗")
    print("██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░██║██╔════╝████╗░██║")
    print("██║░░██║██████╦╝██║░░██║█████╗░░███████║█████╗░░██╔██╗██║")
    print("██║░░██║██╔══██╗██║░░██║██╔══╝░░██╔══██║██╔══╝░░██║╚████║")
    print("██████╔╝██████╦╝╚█████╔╝███████╗██║░░██║███████╗██║░╚███║")
    print("╚═════╝░╚═════╝░░╚════╝░╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝")
    print("       » FB TOKEN EXTRACTOR - BROKEN NADEEM STYLE «")
    print("=========================================================\n")

def get_token_with_email_pass(email, password):
    params = {
        "format": "json",
        "email": email,
        "password": password,
        "credentials_type": "password",
        "generate_session_cookies": 1,
        "error_detail_type": "button_with_disabled",
        "source": "device_based_login",
        "meta_inf_fbmeta": "",
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "locale": "en_US",
        "method": "auth.login"
    }
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; Android 10; Redmi Note 9 Pro Build/QKQ1.191215.002)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive"
    }
    try:
        r = requests.get("https://b-api.facebook.com/method/auth.login", params=params, headers=headers)
        return r.json()
    except Exception as e:
        return {"error_msg": str(e)}

def get_token_from_cookie(cookie):
    headers = {
        "Host": "www.facebook.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 10)",
        "accept": "text/html",
        "cookie": cookie
    }
    try:
        r = requests.get("https://business.facebook.com/business_locations", headers=headers)
        token = re.search(r'EAAG\w+', r.text)
        if token:
            return token.group(0)
        else:
            return None
    except Exception as e:
        return None

def verify_token(token):
    try:
        r = requests.get(f"https://graph.facebook.com/me?access_token={token}")
        return "id" in r.json()
    except:
        return False

def extract_with_email():
    email = input("[?] Enter Facebook Email: ")
    password = input("[?] Enter Facebook Password: ")
    attempt = 1
    while True:
        print(f"\n[!] Attempt {attempt} - Logging in...")
        res = get_token_with_email_pass(email, password)
        if "access_token" in res:
            token = res["access_token"]
            if verify_token(token):
                slow(f"[✓] Token Extracted: {token}", 0.02)
                open("fb_token.txt", "w").write(token)
                print("[+] Token saved to fb_token.txt")
                break
        elif "error_msg" in res and "www.facebook.com" in res["error_msg"]:
            slow("[!] Checkpoint encountered. Approve it manually...", 0.03)
            time.sleep(5)
        else:
            slow(f"[✗] Failed: {res.get('error_msg', 'Unknown error')}", 0.03)
            break
        attempt += 1

def extract_with_cookie():
    cookie = input("[?] Paste your Facebook Cookie: ")
    slow("[*] Extracting token from cookie...", 0.02)
    token = get_token_from_cookie(cookie)
    if token:
        if verify_token(token):
            slow(f"[✓] Token Extracted: {token}", 0.02)
            open("fb_token.txt", "w").write(token)
            print("[+] Token saved to fb_token.txt")
        else:
            slow("[✗] Token received but not valid.", 0.03)
    else:
        slow("[✗] Failed to extract token from cookie.", 0.03)

def main():
    logo()
    print("1. Extract Token via Email & Password")
    print("2. Extract Token via Facebook Cookie")
    choice = input("\n[?] Choose Option (1/2): ")

    if choice == "1":
        extract_with_email()
    elif choice == "2":
        extract_with_cookie()
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
