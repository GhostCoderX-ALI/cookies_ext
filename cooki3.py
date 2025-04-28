import requests
import re
import time

def extract_tokens(html_content):
    # Extract dtsg token
    dtsg_match = re.search(r'"dtsg":{"token":"([^"]+)"', html_content)
    dtsg_token = dtsg_match.group(1) if dtsg_match else None

    # Extract lsd token
    lsd_match = re.search(r'"lsd","token":"([^"]+)"', html_content)
    lsd_token = lsd_match.group(1) if lsd_match else None

    # Extract jazoest token
    jazoest_match = re.search(r'"jazoest","initSprinkleValue":"([^"]+)"', html_content)
    jazoest_token = jazoest_match.group(1) if jazoest_match else None

    return dtsg_token, lsd_token, jazoest_token

def facebook_login(email, password):
    session = requests.Session()

    # Headers for initial request to get tokens
    headers_registration = {
        "sec-ch-ua": '"Not(A:Brand";v="99", "Android WebView";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; M2007J20CG Build/SKQ1.211019.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.137 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "dnt": "1",
        "x-requested-with": "mark.via.gp",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i"
    }

    # Make initial request to get tokens
    response = session.get('https://m.facebook.com/', headers=headers_registration, allow_redirects=False)
    req_html = response.text

    # Extract tokens from HTML content
    dtsg_token, lsd_token, jazoest_token = extract_tokens(req_html)

    if not all([dtsg_token, lsd_token, jazoest_token]):
        print("Failed to extract required tokens from HTML content.")
        return

    # Prepare headers and data for login request
    url = "https://m.facebook.com/login/device-based/login/async/?refsrc=deprecated&lwv=100"

    headers = {
        "sec-ch-ua-platform": "\"Android\"",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Android WebView\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-mobile": "?1",
        "x-asbd-id": "359341",
        "x-fb-lsd": lsd_token,
        "user-agent": "Mozilla/5.0 (Linux; Android 4.4.4; SH-06G Build/SA310) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "*/*",
        "origin": "https://m.facebook.com",
        "x-requested-with": "mark.via.gp",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://m.facebook.com/",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "datr=SprMZ-INRWLnHGNb-fqbIZ9L; sb=VJrMZ5bNaGEc7u3UGseP6zEp; m_pixel_ratio=2.75; wd=393x744; fr=0qeya61pNTLHVRTTx..BnzJpU..AAA.0.0.BnzJrN.AWXRipRM_hs"
    }

    data = {
        "m_ts": "1741462199",
        "li": "t5rMZ_pwaM6Fs1aGE2epaL8l",
        "try_number": "0",
        "unrecognized_tries": "0",
        "email": email,
        "prefill_contact_point": email,
        "prefill_source": "browser_onload",
        "prefill_type": "contact_point",
        "first_prefill_source": "browser_dropdown",
        "first_prefill_type": "contact_point",
        "had_cp_prefilled": "true",
        "had_password_prefilled": "false",
        "is_smart_lock": "false",
        "encpass": "#PWD_BROWSER:0:{}:{}".format(str(int(time.time())), password),
        "fb_dtsg": dtsg_token,
        "jazoest": jazoest_token,
        "lsd": lsd_token,
        "__dyn": "1KQEGiE5q1MzVQ2mmmexu6ErwgE98nwgU2owSwMxW0Oohw5ux60Vo1a852q1ewb60Y82Cwro0wa4o1sE522G0NE2vwSw5Uw4FwmE2ew5fw5NyE1582ZwrU2pw4swSw7zwde",
        "__csr": "",
        "__hsdp": "",
        "__hblp": "",
        "__req": "7",
        "__fmt": "1",
        "__a": "AYmnkRIf6qrw2jSdGAT3JQjESoGPZP3agNDSdXuvkcGyeSuZaTYejWGsNdoyz9kgcmRoNWl0CVJ2PCQkhENpSOimKtdJB07LYXCE3xj0AQTGuw",
        "__user": "0"
    }

    # Make login request
    response = session.post(url, headers=headers, data=data)

    # Check if login was successful
    if "c_user" in session.cookies.get_dict().keys():
        print("Login successful!")

        # Extract session cookies
        cookies = session.cookies.get_dict()
        cookies_string = ";".join([f"{key}={value}" for key, value in cookies.items()])
        print(f"COOKIES: {cookies_string}")
        # Save cookies to file (only once)
        with open('/sdcard/fb_cookies.txt', 'w') as file:
            file.write(cookies_string + "\n")  # Single line with all cookies
            
        print("Session cookies saved to /sdcard/fb_cookies.txt")
    else:
        print("Login failed. Check your credentials or try again later.")

def main():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    facebook_login(email, password)

if __name__ == "__main__":
    main()