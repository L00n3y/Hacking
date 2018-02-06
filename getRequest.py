import requests

payload = {'url' : 'httpL//edge-security.com'}
r = requests.get('http://httpbin.org/redirect-to', params=payload)

print(r.text)
print("Status code:")
print("\t *" + str(r.status_code))
