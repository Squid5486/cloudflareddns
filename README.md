# CloudflareDDNS

This is a simple python script combined with docker that is able to update the ip address in a DNS A record. This allows a cloudflare domain act like dynamic DNS. 

## Setup

Edit the docker-compose.yml file to include a generated Cloudflare API Token, your domain and the record you wish to change. In my case the record name was the same as the domain name. I included a guide below on how to obtain a API Token. 

<pre>version: "3.8"
services:
  cloudflareddns:
    image: cloudflareddns
    build: . 
    container_name: cloudflareddns
    restart: unless-stopped
    environment:
      - TOKEN=token
      - DOMAIN=domain
      - RECORD=record
      - UPDATEINTERVAL=5</pre>

It is even possible to run multiple instances of the script if you wish to update multiple domains.

<pre>version: "3.8"
services:
  domain1:
    image: cloudflareddns
    build: . 
    container_name: domain1
    restart: unless-stopped
    environment:
      - TOKEN=token1
      - DOMAIN=domain1
      - RECORD=record1
      - UPDATEINTERVAL=5
  domain2:
    image: cloudflareddns
    build: . 
    container_name: domain2
    restart: unless-stopped
    environment:
      - TOKEN=token2
      - DOMAIN=domain2
      - RECORD=record2
      - UPDATEINTERVAL=5</pre>

## Getting a the Cloudflare API Token

When updating the Cloudflare dynamic DNS record programmatically, the script must authenticate itself to the Cloudflare API. Only then will Cloudflare allow you to make changes to the DNS records in your account.

Cloudflare allows you to create API tokens with enough permissions for its purpose. In turn, you can then use your API token to authenticate with the Cloudflare API.

To create a Cloudflare API Token, follow these steps.

1. Open your browser, navigate to https://dash.cloudflare.com/login/, and log in to your Cloudflare account.

2. After logging in to the Cloudflare dashboard, click on the profile button on the upper-right corner and click My Profile.

3. Next, click the API Tokens tab link. Under the API Tokens section, click the Create Token button. The example below assumes that you have not created any API tokens yet.

4. On the list of API token templates, click the Edit zone DNS template to use it. This template allows you to create an API token with edit permission to all or selected DNS zones in your account.

5. Under the Zone Resources section on the Create Token page, click the right-most dropdown box and select the DNS zone to include in this API token’s access. After choosing the DNS zone, click Continue to summary.

    Optionally, to limit the API token’s validity period, fill in the Start Date and End Date under the TTL section. If left blank, the API token will have no expiration date. 


6. Review the summary and ensure that the API has DNS:Edit permission to the previously selected DNS zone. Finally, click Create Token to create the API token.

7. After creating the API token, copy the token value and make sure to store it securely. Treat the API token like how you would treat a password.

8. Go back to the API Tokens tab and confirm the existence of the API token you created.
