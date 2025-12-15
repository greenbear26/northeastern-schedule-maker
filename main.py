import requests


# Cookies
session = requests.Session()

base_url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/"

# Step 1
session.get(base_url)
cookies = session.cookies.get_dict()

session_cookie = cookies["JSESSIONID"]
nubanner_cookie = cookies["nubanner-cookie"]

# Step 2
reset_response = session.post(
    f"{base_url}/ssb/classSearch/resetDataForm"
)
print(reset_response.status_code)


# Step 3
post_headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": session_cookie + "; " + nubanner_cookie + ";"
}

post_data = {
    "term": "202630",
    "studyPath": "",
    "studyPathText": "",
    "startDatepicker": "",
    "endDatepicker": ""
}


post = session.post(base_url + "term/search", headers=post_headers, data=post_data)
print(post.headers)
print(post.text)


# url = "https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults"
# payload = {"txt_subject": "CS", "txt_courseNumber": "3100", "txt_term": "202630"}
# response = requests.get(url, params=payload)
# print(response.url)
# print(response.text)
