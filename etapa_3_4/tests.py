import requests

url = "http://localhost:8000/docs"

headers = {
    "Origin": "http://localhost:3001"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

print("CORS:", response.headers.get("Access-Control-Allow-Origin")
)
print("Headers:", response.headers)