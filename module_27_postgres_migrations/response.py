import requests



#https://dummyjson.com/c/3029-d29f-4014-9fb4
RAPID_API_KEY = "3029-d29f-4014-9fb4"

import requests

URL_users = "https://dummyjson.com/users?limit=3"
#headers = {"Authorization": "Bearer /3029-d29f-4014-9fb4/", "Content-Type": "application/json"}
response = requests.get(URL_users)
#print(response.json())
print(len(response.json()["users"]))
result = response.json()
for res1 in result["users"]:
    print(res1["address"])
    #print(f"ФИО: {res1["firstName"]} {res1["lastName"]}\nадрес: {res1["address"]} ")


URL_coffe = "https://dummyjson.com/products/search?q=coffee"
response = requests.get(URL_coffe)
print(len(response.json()['products']))
result_cof = response.json()
for res2 in result_cof['products']:
    #print(res2["reviews"][1]["comment"], res2["reviews"][0]["comment"], res2["reviews"][2]["comment"])
    print(f"Название: {res2['title']}\nCategory: {res2['category']}\nDescription: {res2['description']}\nReviews: {[i["comment"] for i in res2['reviews']]}")






#/* providing access token in bearer */
#fetch('https://dummyjson.com/auth/RESOURCE', {
#  method: 'GET', /* or POST/PUT/PATCH/DELETE */
#  headers: {
#    'Authorization': 'Bearer /* YOUR_ACCESS_TOKEN_HERE */',
#    'Content-Type': 'application/json'
#  },
#})
# #.then(res => res.json())
#.then(console.log);
