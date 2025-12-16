import requests


base_url = "https://nubanner.neu.edu/StudentRegistrationSsb/"

session = requests.Session()

# Cookies
session.get(base_url)
client_cookie = session.cookies.get_dict().get("JSESSIONID")
nubanner_cookie = session.cookies.get_dict().get("nubanner-cookie")
print(f"Client Cookie: {client_cookie}")
print(f"NUBanner Cookie: {nubanner_cookie}")

# Reset
reset_header = {
    "Cookie": f"JSESSIONID={client_cookie}; nubanner-cookie={nubanner_cookie}"
}
reset_response = session.post(base_url + "ssb/classSearch/resetDataForm", headers=reset_header)
print(f"Reset Status Code: {reset_response.status_code}")
print(f"Reset Response: {reset_response.text}")

# # Test: term options
# term_params = {
#     "term": "202630",
#     "offset": "1",
#     "max": "1000",
#     "searchTerm": ""
# }
# term_response = requests.get(base_url + "classSearch/get_subject", params=term_params)
# print(f"Term Options Status Code: {term_response.status_code}")
# print(f"Term Options Response: {term_response.text}")



# Term Declaration
term_header = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UT",
    "Cookie": f"JSESSIONID={client_cookie}; nubanner-cookie={nubanner_cookie}"
}
term_body = {
    "term": "202630",
    "studyPath": "",
    "studyPathText": "",
    "studyDatepicker": "",
    "endDatePicker": "",
}
term_response = session.post(base_url + "ssb/term/search?mode=search", data=term_body)
print(f"Term Status Code: {term_response.status_code}")
print(f"Term Response: {term_response.text}")

# Pull Class data
class_header = {
    "Cookie": f"JSESSIONID={client_cookie}; nubanner-cookie={nubanner_cookie}"
}
class_params = {
    "txt_subject": "CS",
    "txt_courseNumber": "3100",
    "txt_term": "202630",
    # "startDatepicker": "",
    # "endDatePicker": "",
    # "pageOffset": "0",
    # "pageMaxSize": "1000",
    # "sortColumn": "subjectDescription",
    # "sortDirection": "asc",
}
class_response = session.get(base_url + "ssb/searchResults/searchResults",
                              params=class_params, headers=class_header)
print(f"Class Status Code: {class_response.status_code}")
print(f"Class Response: {class_response.text}")


#Specific Class Info
specific_class_header = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UT"
}
specific_class_body = {
    "term": "202630",
    "courseReferenceNumber": "36060",
}
specific_class_response = session.get(base_url +
    "ssb/searchResults/getFacultyMeetingTimes", params=specific_class_body, headers=specific_class_header)
print(f"Specific Class Status Code: {specific_class_response.status_code}")
print(f"Specific Class Response: {specific_class_response.text}")
