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
    def is_valid(section) -> bool:
        return section.available_slots > 0

    def is_conflict(new_section, current_section) -> bool:
        if new_section == current_section:
            return True
        if new_section.campus != current_section.campus:
            return True

        for day in new_section.days:
            if day in current_section.days:
                # Check for time overlap
                if (new_section.start_time < current_section.end_time and
                    new_section.end_time > current_section.start_time):
                    return True
        return False

    def backtrack(all_schedules, current_schedule, course_index):
        # Base case: all courses have been scheduled
        if course_index == len(courses):
            if len(current_schedule) == len(courses):
                all_schedules.append(current_schedule)
            return all_schedules

        # Try to schedule each section of the current course
        for section in courses[course_index]:
            # Check if section is valid
            if not is_valid(section):
                continue

            # Check for conflicts with already scheduled sections
            conflict = False
            for scheduled_section in current_schedule.values():
                if is_conflict(section, scheduled_section):
                    conflict = True
                    break

            # If no conflict, add section to schedule and recurse
            if not conflict:
                current_schedule[courses[course_index]] = section
                backtrack(all_schedules, current_schedule, course_index + 1)
                current_schedule.pop(courses[course_index])
        return all_schedules

    all_schedules = []
    all_schedules = backtrack(all_schedules, {}, 0)

    for i, current_schedule in enumerate(all_schedules):
        for course, section in current_schedule.items():
            print(f"{course.code}: {str(section)}")

    return all_schedules
    
with requests.Session() as session:
    course_getter = CourseGetter(session, "202630")

    courses = []
    course_codes = ["CY2550", "CS3100", "COMM1210"]
    for code in course_codes:
        course = course_getter.get_course(code)
        courses.append(course)

    for course in courses:
        print(f"Course {course.code} has {len(course.sections)} sections.")

    schedules = make_schedules(courses)
    print(f"Generated {len(schedules)} possible schedules.")
    for schedule in schedules:
        # print(f"\nSchedule {i + 1}:")
        for course in courses:
            section = schedule.get(course)
            if section:
                print(f"{course.code}: {str(section)}")
