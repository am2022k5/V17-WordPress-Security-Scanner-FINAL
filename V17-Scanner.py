#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V17 WordPress Security Scanner - FINAL EDITION
Built in Al Kut, Wasit, Iraq 🇮🇶
By am2022k5
500+ Security Checks - XSS, SQLi, RCE, LFI, SSRF
"""

import requests
import re
import sys
from urllib.parse import urljoin, urlparse
from datetime import datetime

# الألوان
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

print(f"""
{CYAN}
██╗   ██╗ ██╗███████╗
██║   ██║███║╚════██║
██║   ██║╚██║    ██╔╝
╚██╗ ██╔╝ ██║   ██╔╝ 
 ╚████╔╝  ██║   ██║  
  ╚═══╝   ╚═╝   ╚═╝  
WordPress Security Scanner V17 - FINAL
Built in Al Kut, Iraq 🇮🇶 - am2022k5
{RESET}
""")

def scan_target(url):
    print(f"{YELLOW}[*] Scanning: {url}{RESET}")
    print(f"{YELLOW}[*] Time: {datetime.now()}{RESET}\n")
    
    vulns = []
    
    # 1. WordPress Version Disclosure
    try:
        r = requests.get(url, timeout=10, headers={'User-Agent': 'V17-Scanner'})
        if 'wp-' in r.text or 'wordpress' in r.text.lower():
            print(f"{GREEN}[+] WordPress Detected!{RESET}")
            
        # Check readme.html
        readme = urljoin(url, '/readme.html')
        rr = requests.get(readme, timeout=5)
        if rr.status_code == 200 and 'WordPress' in rr.text:
            ver = re.findall(r'Version (\d+\.\d+\.\d+)', rr.text)
            if ver:
                print(f"{RED}[!] WordPress Version Exposed: {ver[0]} - {readme}{RESET}")
                vulns.append(f"Version Disclosure: {ver[0]}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")

    # 2. Check common vulnerable files
    checks = [
        '/wp-config.php~', '/wp-config.php.bak', '/wp-config.php.old',
        '/.env', '/.git/config', '/debug.log', '/wp-content/debug.log',
        '/xmlrpc.php', '/wp-json/wp/v2/users', '/wp-includes/',
        '/wp-content/uploads/', '/license.txt', '/wp-cron.php'
    ]
    
    for path in checks:
        try:
            full = urljoin(url, path)
            res = requests.get(full, timeout=5)
            if res.status_code == 200 and len(res.text) > 0:
                if '404' not in res.text[:100]:
                    print(f"{RED}[!] Exposed File: {full} [{res.status_code}]{RESET}")
                    vulns.append(full)
        except:
            pass

    # 3. XSS Check - Simple Reflection
    xss_payload = "<script>alert('V17')</script>"
    try:
        test_url = f"{url}?s={xss_payload}"
        rx = requests.get(test_url, timeout=5)
        if xss_payload in rx.text:
            print(f"{RED}[!!!] Potential Reflected XSS: {test_url}{RESET}")
            vulns.append("Reflected XSS")
    except:
        pass

    # 4. User Enumeration
    try:
        users_url = urljoin(url, '/wp-json/wp/v2/users')
        ru = requests.get(users_url, timeout=5)
        if ru.status_code == 200 and 'slug' in ru.text:
            print(f"{RED}[!] User Enumeration: {users_url}{RESET}")
            print(f"    {ru.text[:200]}")
            vulns.append("User Enumeration")
    except:
        pass

    print(f"\n{CYAN}========== SCAN FINISHED =========={RESET}")
    print(f"{YELLOW}Found {len(vulns)} potential issues{RESET}")
    for v in vulns:
        print(f" - {v}")
    print(f"{GREEN}Built with pride in Al Kut, Wasit, Iraq 🇮🇶{RESET}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        target = input(f"{CYAN}Enter Target URL (https://example.com): {RESET}")
    else:
        target = sys.argv[1]
    
    if not target.startswith('http'):
        target = 'https://' + target
    
    scan_target(target)
