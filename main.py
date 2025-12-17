import requests
from get_course import CourseGetter

if __name__ == "__main__":
    with requests.Session() as session:
        course_getter = CourseGetter(session, "202630")
        course = course_getter.get_course("COMM1210")
        print(course)
        course2 = course_getter.get_course("CY2550")
        print(course2)

        # courses = []
        # courses.append(get_course(session, "202630", "COMM1210")))
        # courses.append(get_course(session, "202630", "COMM1210")))
        # courses.append(get_course(session, "202630", "COMM1210")))
        # courses.append(get_course(session, "202630", "COMM1210")))
