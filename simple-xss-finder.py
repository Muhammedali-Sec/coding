from urllib.parse import urlparse, parse_qs, urlencode
import requests
url = input("Enter the url you want to test:")
payload = "<script>alert(1)</script>"
def xssfinder(url, payload):
    parse = urlparse(url)
    params = parse_qs(parse.query)
    
    if parse.scheme not in ["http", "https"]:
        print("the url is invalid")
        return
    
    test_response = requests.get(url)
    if test_response.status_code == 404:
        print("the url is returning 404")
        return
    
    if not params:
        print("[-] No parameters found")
        return
    
    for param in params:
        print(f"[+] Injecting the payload to {param} parameter")
        newparam = params.copy()
        newparam[param] = [payload]

        encoded_query = urlencode(newparam, doseq=True)
        new_url = f"{parse.scheme}://{parse.netloc}{parse.path}?{encoded_query}"
        print("Url:", new_url)

        try:
            response = requests.get(new_url)
            raw = response.text

            if payload in raw:
                print(f"[!] Possible XSS in {param}")
            else:
                print(f"[-] {param} does not reflect the payload")
        except Exception as e:
            print("Request error:", e)
xssfinder(url, payload)         
