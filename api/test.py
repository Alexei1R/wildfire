import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Your client credentials
client_id = 'sh-3439580d-a09f-4e5c-b7d4-a6d6ff6f72f7'
client_secret = '0rTZiejJzmWEsRxT81c4ytdTExGJTTYC'

# Create a session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

# Fetch the token
token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
token = oauth.fetch_token(token_url=token_url, client_secret=client_secret, include_client_id=True)

print("Access Token:", token['access_token'])

# Test WMS Instances API
wms_url = "https://sh.dataspace.copernicus.eu/configuration/v1/wms/instances"
resp = oauth.get(wms_url)

if resp.status_code == 200:
    print("WMS Instances Response:", resp.json())
else:
    print(f"Error: {resp.status_code} - {resp.text}")

# Make a POST request with data
search_url = "https://sh.dataspace.copernicus.eu/api/v1/search"  # Example search endpoint
data = {
    "bbox": [13, 45, 14, 46],
    "datetime": "2019-12-10T00:00:00Z/2019-12-10T23:59:59Z",
    "collections": ["sentinel-1-grd"],
    "limit": 5,
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token['access_token']}",
}

search_resp = requests.post(search_url, json=data, headers=headers)

if search_resp.status_code == 200:
    print("Search Response:", search_resp.json())
else:
    print(f"Search Error: {search_resp.status_code} - {search_resp.text}")

# url = "https://sh.dataspace.copernicus.eu/api/v1/catalog/1.0.0/search"
# response = requests.post(url, json=data)
# print(response.content)

# url = "https://sh.dataspace.copernicus.eu/api/v1/process"
# headers = {
#   "Content-Type": "application/json",
#   "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJYVUh3VWZKaHVDVWo0X3k4ZF8xM0hxWXBYMFdwdDd2anhob2FPLUxzREZFIn0.eyJleHAiOjE3MzIzNzcyODgsImlhdCI6MTczMjM3NjY4OCwiYXV0aF90aW1lIjoxNzMyMzc2NTk5LCJqdGkiOiIyOGU0NGMxMy1mMzQwLTRiNjItYjZmYi04YjQxMWE1YzkzMGMiLCJpc3MiOiJodHRwczovL2lkZW50aXR5LmRhdGFzcGFjZS5jb3Blcm5pY3VzLmV1L2F1dGgvcmVhbG1zL0NEU0UiLCJzdWIiOiIzNDllOTUwYi05ZmI4LTRjMDEtOTk4Yi0xZTA4ZTU0M2YxYjEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJzaC0yZDA3NzkxNy1lZTZlLTQyOGUtODZiZC1lZjNmOWVlNGUyZTEiLCJub25jZSI6IjgyMTY2ZDRjLTdkMGYtNDBjMy05NThiLTA1ZmIyODY4ZDBkNiIsInNlc3Npb25fc3RhdGUiOiIxMzFiZGM0Yi0yMDBiLTQ2Y2UtYTQ5Ny0zMGQxNzI0ZjkxNjUiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9zaGFwcHMuZGF0YXNwYWNlLmNvcGVybmljdXMuZXUiXSwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSB1c2VyLWNvbnRleHQiLCJzaWQiOiIxMzFiZGM0Yi0yMDBiLTQ2Y2UtYTQ5Ny0zMGQxNzI0ZjkxNjUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwib3JnYW5pemF0aW9ucyI6WyJkZWZhdWx0LTM0OWU5NTBiLTlmYjgtNGMwMS05OThiLTFlMDhlNTQzZjFiMSJdLCJuYW1lIjoiUnVzdSBBbGV4ZWkiLCJ1c2VyX2NvbnRleHRfaWQiOiIwY2U3MWRmMS0xYTFhLTQxMTUtYTk0OS0yZjY4MDRlZjk1MjEiLCJjb250ZXh0X3JvbGVzIjp7fSwiY29udGV4dF9ncm91cHMiOlsiL2FjY2Vzc19ncm91cHMvdXNlcl90eXBvbG9neS9jb3Blcm5pY3VzX2dlbmVyYWwvIiwiL29yZ2FuaXphdGlvbnMvZGVmYXVsdC0zNDllOTUwYi05ZmI4LTRjMDEtOTk4Yi0xZTA4ZTU0M2YxYjEvcmVndWxhcl91c2VyLyJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhbGV4ZWkucnVzdS4yMDAyQGdtYWlsLmNvbSIsImdpdmVuX25hbWUiOiJSdXN1IiwidXNlcl9jb250ZXh0IjoiZGVmYXVsdC0zNDllOTUwYi05ZmI4LTRjMDEtOTk4Yi0xZTA4ZTU0M2YxYjEiLCJmYW1pbHlfbmFtZSI6IkFsZXhlaSIsImVtYWlsIjoiYWxleGVpLnJ1c3UuMjAwMkBnbWFpbC5jb20ifQ.KdV7SmQ_4_fdaB8FbXirT1RAZ9-Fm3JXvPINyOwg1VExFPoNqDa3L9iCDpffLYImO4dzE7rlDPpzcPlz69jJLz7GOKsbKBVp66Zhay3is8joARFQHve-OgvqQxUCeDXNLh_4HEN4p74eYIkITsPuwj7MumnNDmAkzyzeRbwWxhzzBUtMrNGsO6Pgtmj2eJ91xVEhhUK0nzxBZIRxHyDnYAOHBqt4vZYrJ_IpWB6-DwScqvvpe2ebaZ-RBxDvYTJMaVEmMhmUH_z3MCAPg5CrxJ1KR1KwHS3A1aS7pWRRtPyez6eqcH7HouHIe2lz72mqwe5tckL-_2qMkppAFIzMEg"
# }
# data = {
#   "input": {
#     "bounds": {
#       "bbox": [
#         12.44693,
#         41.870072,
#         12.541001,
#         41.917096
#       ]
#     },
#     "data": [
#       {
#         "dataFilter": {
#           "timeRange": {
#             "from": "2024-10-23T00:00:00Z",
#             "to": "2024-11-23T23:59:59Z"
#           }
#         },
#         "type": "sentinel-2-l2a"
#       }
#     ]
#   },
#   "output": {
#     "width": 512,
#     "height": 343.697,
#     "responses": [
#       {
#         "identifier": "default",
#         "format": {
#           "type": "image/jpeg"
#         }
#       }
#     ]
#   },
#   "evalscript": "//VERSION=3\n\nfunction setup() {\n  return {\n    input: [\"B02\", \"B03\", \"B04\"],\n    output: { bands: 3 }\n  };\n}\n\nfunction evaluatePixel(sample) {\n  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];\n}"
# }
#
# response = requests.post(url, headers=headers, json=data)
#
#
# # print(response.headers)
#
# print(response.content)
