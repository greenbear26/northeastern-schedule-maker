import requests
from get_course import CourseGetter
from get_schedules import ScheduleGetter

    



with requests.Session() as session:
    # Set courses
    course_getter = CourseGetter(session, "202630")

    courses = []
    course_codes = ["CY2550", "CS3100", "COMM1210"]
    for code in course_codes:
        course = course_getter.get_course(code)
        courses.append(course)

    for course in courses:
        print(f"Course {course.code} has {len(course.sections)} sections.")

    # Generate schedules
    schedule_getter = ScheduleGetter(courses)
    schedules = schedule_getter.make_schedules()

    print(f"\nGenerated {len(schedules)} possible schedules:")

    for i, current_schedule in enumerate(schedules):
        print(f"\nSchedule {i + 1}:")
        for section in current_schedule:
            print(f"{section.code}: {str(section)}")
