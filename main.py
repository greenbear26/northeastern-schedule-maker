import requests
from get_course import get_course

if __name__ == "__main__":
    with requests.Session() as session:
        print(get_course(session, "202630", "COMM1210"))
