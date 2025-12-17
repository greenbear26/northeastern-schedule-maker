import requests
from get_course import CourseGetter

def make_schedules(course: "Course[]") -> "dict(Course, Section)[]":
    """Generates all possible non-conflicting schedules from the provided courses.

    Params
    ------------
    courses : Course[]
        A list of Course objects to generate schedules from.

    Returns
    ------------
    Course[][]
        A list of possible schedules, where each schedule is a list of Course
        objects with selected Sections in a dictionary.
    """
    def is_conflict(section1, section2) -> bool:
        # # Check for day overlap
        # if not set(section1.days).intersection(set(section2.days)):
        #     return False

        # # Check for time overlap
        # latest_start = max(section1.start_time, section2.start_time)
        # earliest_end = min(section1.end_time, section2.end_time)
        # return latest_start < earliest_end
        return False

    def backtrack(current_schedule, course_index):
        # Base case: all courses have been scheduled
        if course_index == len(courses):
            if len(current_schedule) == len(courses):
                print("Found valid schedule:")
                for course, section in current_schedule.items():
                    print(f"{course.code}: {str(section)}")
                all_schedules.append(current_schedule)
            return

        # Try to schedule each section of the current course
        for section in courses[course_index]:
            # Check for conflicts with already scheduled sections
            conflict = False
            for scheduled_section in current_schedule.values():
                if is_conflict(section, scheduled_section):
                    conflict = True
                    break

            # If no conflict, add section to schedule and recurse
            if not conflict:
                current_schedule[courses[course_index]] = section
                backtrack(current_schedule, course_index + 1)
                current_schedule.pop(courses[course_index])

    all_schedules = []
    backtrack({}, 0)
    return all_schedules
    
with requests.Session() as session:
    course_getter = CourseGetter(session, "202630")

    courses = []
    course_codes = ["CY2550", "CS3100", "COMM1210", "MATH1465"]
    for code in course_codes:
        course = course_getter.get_course(code)
        courses.append(course)

    for course in courses:
        print(f"Course {course.code} has {len(course.sections)} sections.")

    schedules = make_schedules(courses)
    print(f"Generated {len(schedules)} possible schedules.")
    # for i, schedule in enumerate(schedules):
    #     print(f"\nSchedule {i + 1}:")
    #     for course, section in schedule.items():
    #         print(f"{course.code}: {section}")
