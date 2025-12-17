from course_sections import Course, Section, Days
import requests


base_url = "https://nubanner.neu.edu/StudentRegistrationSsb/"

def get_course_sections(session, term: str, course_code: str):
    course = Course(course_code)

    client_cookie = session.cookies.get_dict().get("JSESSIONID")
    nubanner_cookie = session.cookies.get_dict().get("nubanner-cookie")

    # Reset
    reset_header = {
        "Cookie": f"JSESSIONID={client_cookie}; nubanner-cookie={nubanner_cookie}"
    }
    session.post(base_url + "ssb/classSearch/resetDataForm", headers=reset_header)

    # Term Declaration
    term_header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UT",
        "Cookie": f"JSESSIONID={client_cookie}; nubanner-cookie={nubanner_cookie}"
    }
    term_body = {
        "term": term,
        "studyPath": "",
        "studyPathText": "",
        "studyDatepicker": "",
        "endDatePicker": "",
    }
    session.post(base_url + "ssb/term/search?mode=search", data=term_body)

    # Pull Course data
    course_header = {
        "Cookie": f"JSESSIONID={client_cookie}; nubanner-cookie={nubanner_cookie}"
    }

    # Extract subject code and course number
    subject_code = ""
    for i, char in enumerate(course_code):
        if char.isdigit():
            subject_code = course_code[:i]
            break
    course_number = course_code[i:]

    course_params = {
        "txt_subject": subject_code,
        "txt_courseNumber": course_number,
        "txt_term": term,
    }
    course_response = session.get(base_url + "ssb/searchResults/searchResults",
                                  params=course_params, headers=course_header)

    data = course_response.json().get("data", [])

    if data is None:
        print("No data found for the specified course.")
        return

    for section_data in data:
        available_slots = section_data.get("seatsAvailable", 0)
        reference_number = section_data.get("courseReferenceNumber", "")
        campus = section_data.get("campusDescription", "")

        days = []
        start_time = ""
        end_time = ""
        meeting_times = section_data.get("meetingsFaculty", [])
        if meeting_times:
            faculty_dict = meeting_times[0]
            meeting_time = faculty_dict.get("meetingTime", {})
            for day in Days:
                if meeting_time.get(day.value, False):
                    days.append(day)

            start_time = meeting_time.get("beginTime", "")
            end_time = meeting_time.get("endTime", "")

        if days and start_time and end_time and reference_number:
            section = Section(
                reference_number=int(reference_number),
                campus=campus,
                days=days,
                start_time=start_time,
                end_time=end_time,
                available_slots=int(available_slots)
            )
            course.add_section(section)

    print(course)


if __name__ == "__main__":
    with requests.Session() as session:
        session.get(base_url)
        get_course_sections(session, term="202630", course_code="CS3000")
        get_course_sections(session, term="202630", course_code="CS3100")
        # get_course_sections(session, term="202630", course_code="EECE2310")
        # get_course_sections(session, term="202630", course_code="EECE2311")

