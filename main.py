import requests
from get_sections import get_course_sections

if __name__ == "__main__":
    with requests.Session() as session:
        print(get_course_sections(session, "202630", "CY2550"))

