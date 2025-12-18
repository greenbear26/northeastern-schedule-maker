import sys
import requests
from get_course import CourseGetter
from get_schedules import ScheduleGetter

if len(sys.argv) < 3:
    print("Usage: python main.py <term> <course_code1> <course_code2> ...")
    print("Example: python main.py 202630 CY2550 CS3100 COMM1210")
    sys.exit(1)

with requests.Session() as session:
    # Set courses
    course_getter = CourseGetter(session, sys.argv[1])

    courses = []
    course_codes = sys.argv[2:]
    for code in course_codes:
        course = course_getter.get_course(code)
        courses.append(course)

    # Generate schedules
    schedule_getter = ScheduleGetter(courses)
    schedules = schedule_getter.make_schedules()

    print(f"Generated {len(schedules)} possible schedules:")

    for i, current_schedule in enumerate(schedules):
        print(f"\nSchedule {i + 1}:")
        for section in current_schedule:
            print(f"{section.code}: {str(section)}")
