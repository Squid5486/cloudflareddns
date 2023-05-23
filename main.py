import requests
import json
import os # to be able to access environment variables
import schedule
import time

# Input parameters
token = os.getenv('TOKEN', '')
domain = os.getenv('DOMAIN', '')
record = os.getenv('RECORD', '')
updateinterval = os.getenv('UPDATEINTERVAL', '5') # interval in minutes. default: 5


# Build the request headers
headers = {
    # "X-Auth-Email": email,
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

# Token Test
uri = "https://api.cloudflare.com/client/v4/user/tokens/verify"
auth_result = json.loads(requests.get(uri, headers=headers).text)

if not auth_result["result"]:
    print(f"API token validation failed. Error: {auth_result['errors'][0]['message']}. Terminating script.")
    exit()

print(f"API token validation [{token}] success. {auth_result['messages'][0]['message']}.")


def updateAddress():
    # Get Zone ID
    uri = f"https://api.cloudflare.com/client/v4/zones?name={domain}"
    dns_zone = requests.get(uri, headers=headers).json()

    if not dns_zone["result"]:
        print(f"Search for the DNS domain [{domain}] returned zero results. Terminating script.")
        exit()

    zone_id = dns_zone["result"][0]["id"]
    print(f"Domain zone [{domain}]: ID={zone_id}")

    # Get DNS Record
    uri = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={record}"
    dns_record = requests.get(uri, headers=headers).json()

    if not dns_record["result"]:
        print(f"Search for the DNS record [{record}] returned zero results. Terminating script.")
        exit()

    old_ip = dns_record["result"][0]["content"]
    record_type = dns_record["result"][0]["type"]
    record_id = dns_record["result"][0]["id"]
    record_ttl = dns_record["result"][0]["ttl"]
    record_proxied = dns_record["result"][0]["proxied"]
    print(f"DNS record [{record}]: Type={record_type}, IP={old_ip}")

    # Get Current Public IP Address
    new_ip = requests.get('https://v4.ident.me').text
    # new_ip = "223.233.233.123"
    print(f"Public IP Address: OLD={old_ip}, NEW={new_ip}")

    # Update Dynamic DNS Record
    if new_ip != old_ip:
        print("The current IP address does not match the DNS record IP address. Attempting to update.")
        uri = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
        body = {
            "type": record_type,
            "name": record,
            "content": new_ip,
            "ttl": record_ttl,
            "proxied": record_proxied
        }

        update = json.loads(requests.put(uri, headers=headers, json=body).text)

        if "errors" in update:
            print(f"DNS record update failed. Error: {update['errors']}")
            exit()

        print("DNS record update successful.")
        exit(update["result"])
    else:
        print("The current IP address and DNS record IP address are the same. There's no need to update.")



schedule.every(int(updateinterval)).minutes.do(updateAddress)
print(f"updateinterval is set to {updateinterval} minutes")

while True:
    schedule.run_pending()
    time.sleep(1)