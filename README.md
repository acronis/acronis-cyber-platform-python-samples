# Acronis Cyber Platform Python Samples

This repository provides a set of easy to understand and tested Python samples for using [Acronis Cyber Platform API](https://developer.acronis.com/doc).

If you have any question regarding Acronis Cyber Platform API samples or usage, please check the documentations at [Acronis Developer Network portal](https://developer.acronis.com/) or use [Acronis Cyber Platform Forum](https://forum.acronis.com/forum/acronis-cyber-platform-forum-apis-and-sdks/acronis-cyber-platform-forum-apis-and-sdks).

## How to use samples

**_Notice_**: _to successfully run samples Python version >= 3.6 is required_

To use those samples in your environment you should have pre-requirements installed.

```txt
pytest>=5.1.0
requests>=2.22.0
argparse>=1.4.0
jsonschema>=3.0.2
```

To install those requirements, you can use provided requirements.txt

```bash
pip install -r requirements.txt
```

To use samples, move to the directory which contains the sample you want to run. Than run appropriate python script with all needed parameters.

Most of scripts, just collect parameters and make corresponding API call directly with appropriate HTTP method, API endpoint URI and an authentication token received by Client during initialization based on data in config.json file.

## Acronis Cyber Platform API client and authentication

The samples use a Client object defines in client.py in the root directory of the repository. The Client uses config.json to  initialize a Client instance. You should provide information in config.json file like shown below.

```JSON
{
  "login": "<your_login>",
  "password": "<your_password>",
  "router_url": "https://beta-cloud.acronis.com/api/1/accounts",
  "client_id": "<client_id>",
  "client_secret": "<client_secret>"
}
```

| Parameter        | Mearning       |Required|
| ------------- |-------------|:-------------:|
| login      | The login the administrator account  | Yes
| password      | The password the administrator account | Yes
| router_url      | An url to receive actual base url for API calls  | Yes
| client_id      | The registered client_id for your application | Yes
| client_secret      | The secret for the registered application | Yes

---

**_Notice_**: _A real application must securely store the client’s secret, login and password values. Exposing these values may allow an attacker to perform malicious or destructive operations within the tenant that this application manages._

---
To receive client_id and client_secret you need to create a new client representing your application in the platform. It will be bounded to the specified tenant, and assigned the same rights as the specified account.

Here you can find code example how to obtain client_id and client_secret.

```python
credentials = '<your_login>', '<your_password>'
tenant_id = '<your_tenant_guid>'
base_url = '<base_url_for_api_calls>'

client = {
          'type': 'agent',
          'tenant_id': tenant_id,
          'token_endpoint_auth_method': 'client_secret_basic',
          'data': {'name': '<your_app_name>'},
}

# Register the application as a client in the cloud platform by sending the POST request to the /clients  # endpoint. The request should use the Basic authentication scheme and contain the account credentials.

# The requests module will automatically encode the credentials into Base64, construct the Authorization # header with the encoded credentials, and add this header to the request. The module will also convert
# the client object to a valid JSON object.
response = requests.post(f'{base_url}/clients', auth=credentials, json=client)

# The 201 code means that a new client representing the application has been created in the platform,
# bound to the specified tenant, and assigned the same rights as the specified account.
# A different code means that an error has occurred.
if response.status_code == 201:
    data = response.json()
    client_id = data['client_id']
    client_secret = data['client_secret']
```

The Client in client.py uses client_id and client_secret to obtain token for further authentication for API calls.
