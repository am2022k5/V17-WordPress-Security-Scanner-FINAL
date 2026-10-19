import requests
import re
import sys
from urllib.parse import urljoin
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def banner():
    print(f"""{CYAN}
 ██    ██  ██ ████████ 
 ██    ██ ███    ██    
 ██    ██  ██    ██    
  ██  ██   ██    ██    
   ████    ██    ██    
    ██     ██    ██    
WordPress Security Scanner V17.1 - FINAL
Built in Al Kut, Iraq IQ - am2022k5
{RESET}""")

def scan_target(url):
    if not url.startswith('http'):
        url = 'https://' + url
    target = url.rstrip('/')
    print(f"{YELLOW}[*] Scanning: {target}{RESET}")
    print(f"{YELLOW}[*] Time: {datetime.now()}{RESET}\n")
    vulns = []
    try:
        r = requests.get(target, timeout=20, verify=False)
        if 'wp-' in r.text or 'wordpress' in r.text or 'wp-content' in r.text:
            print(f"{GREEN}[+] WordPress Detected!{RESET}")
        readme = urljoin(target, '/readme.html')
        rr = requests.get(readme, timeout=15, verify=False)
        if rr.status_code == 200 and 'WordPress' in rr.text:
            ver = re.findall(r'Version (\d+\.\d+\.\d+)', rr.text)
            if ver:
                print(f"{RED}[!] WordPress Version: {ver[0]}{RESET}")
                vulns.append(f"Version Disclosure: {ver[0]}")
        checks = ['/wp-config.php~', '/wp-config.php.bak', '/wp-config.bak', '/.env', '/.git/config', '/debug.log']
        for path in checks:
            try:
                cr = requests.get(urljoin(target, path), timeout=15, verify=False)
                if cr.status_code == 200 and len(cr.text) > 10 and len(cr.text) < 5000:
                    if 'DB_PASSWORD' in cr.text or 'DB_NAME' in cr.text or '<?php' in cr.text:
                        print(f"{RED}[!!!] CRITICAL FILE EXPOSED: {path}{RESET}")
                        vulns.append(f"Exposed: {path}")
            except: pass
        users_url = urljoin(target, '/wp-json/wp/v2/users')
        ur = requests.get(users_url, timeout=15, verify=False)
        if ur.status_code == 200 and 'slug' in ur.text:
            print(f"{RED}[!] User Enumeration Possible: /wp-json/wp/v2/users{RESET}")
            vulns.append("User Enumeration")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")
    print(f"\n{CYAN}=========== SCAN FINISHED ==========={RESET}")
    print(f"{YELLOW}Found {len(vulns)} potential issues{RESET}")
    print(f"{GREEN}Built with pride in Al Kut, Wasit, Iraq | am2022k5{RESET}")
    return vulns

if __name__ == "__main__":
    banner()
    if len(sys.argv) > 1:
        scan_target(sys.argv[1])
    else:
        t = input(f"{CYAN}Enter Target URL: {RESET}")
        scan_target(t)
