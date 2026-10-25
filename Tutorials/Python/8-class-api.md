# What is the `requests` package?

The `requests` package is a `third-party Python library` used to `send HTTP requests` to servers and receive responses.

## Install the package

```
pip install requests
```

Then import it:

```
import requests
```

## Make your first GET request

A GET request is used to retrieve data from a server.

```py
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print(response.status_code)
print(response.text) # response body as text.

print(response.json()) # parses a JSON response into Python objects, typically a dictionary or list.

# {'userId': 1, 'id': 1, 'title': 'sunt aut', 'body': 'quia et...'}

```
## Example of a POST request:

```py
import requests

url = "https://jsonplaceholder.typicode.com/posts"

data = {
    "title": "Learning Python",
    "body": "Understanding requests package",
    "userId": 1
}

# Here, `json=data` sends the Python dictionary as a JSON request body.
response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
```

## Handle errors properly

A request can fail because of network problems, an invalid URL, or an unsuccessful HTTP status.

```py
import requests

try:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=10 # — limits how long the client waits for the request to complete, in seconds.
    )

    response.raise_for_status() # — raises an HTTP error for unsuccessful status codes such as `404` or `500`.
    data = response.json()
    print(data)

except requests.exceptions.Timeout:
    print("The request timed out.")

except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)

except requests.exceptions.RequestException as error:
    print("Request failed:", error)
```

Two important concepts:

- `timeout=10` — limits how long the client waits for the request to complete, in seconds.
- `raise_for_status()` — raises an HTTP error for unsuccessful status codes such as `404` or `500`.

-------

# urllib - Python Inbuilt package for HTTP Calls

Python's standard library includes `urllib.request` for making HTTP requests.

## GET API

```py
import urllib.request
import json

url = "https://jsonplaceholder.typicode.com/posts/1"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))
    print(data)
```

**This code:**
- urlopen(url) sends an HTTP GET request.
- response.read() reads the response bytes.
- .decode("utf-8") converts bytes into a string.
- json.loads() converts the JSON string into a Python dictionary.


## POST API - 

```py
import urllib.request
import json

url = "https://jsonplaceholder.typicode.com/posts"

data = {
    "title": "Learning Python",
    "body": "Understanding urllib",
    "userId": 1
}

# Convert Python dictionary to JSON bytes
json_data = json.dumps(data).encode("utf-8")

# Create POST request
request = urllib.request.Request(
    url,
    data=json_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

# Send request and read response
with urllib.request.urlopen(request) as response:
    print("Status:", response.status)

    result = json.loads(response.read().decode("utf-8"))
    print("Response:", result)
```

-----------