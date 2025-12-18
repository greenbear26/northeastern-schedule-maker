from course_sections import Course, Section, Days
import requests


class CourseGetter:
    """Fetches course sections from the Northeastern University Banner system

    Params
    ------------
    session : requests.Session
        An active requests session to maintain cookies and headers.
    term : str
        The term code (e.g., "202630" for Spring 2026).
    """
    BASE_URL = "https://nubanner.neu.edu/StudentRegistrationSsb/"

    def __init__(self, session: requests.Session, term: str):
        self._session = session
        self._term = term
        self._is_initialized = False

    def _initialize(self):
        if self._is_initialized:
            return
        # Term Declaration
        term_body = {
            "term": self._term,
            "studyPath": "",
            "studyPathText": "",
            "studyDatepicker": "",
            "endDatePicker": "",
        }
        self._session.post(CourseGetter.BASE_URL + "ssb/term/search?mode=search", 
                           data=term_body)
        self._is_initialized = True

    def get_course(self, course_code: str) -> Course:
        """Fetches and returns the sections for a given course code and term.

        Params
        ------------
        session : requests.Session
            An active requests session to maintain cookies and headers.
        term : str
            The term code (e.g., "202630" for Spring 2026).
        course_code : str
            The course code (e.g., "CY2550").

        Returns
        ------------
        Course
            An object containing the sections of the specified course.
        """
        self._initialize()
        # Initialize Course object
        course = Course(course_code)

        # Reset Request
        self._session.post(CourseGetter.BASE_URL + "ssb/classSearch/resetDataForm")

        # Pull Course data

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
            "txt_term": self._term,
        }
        course_response = self._session.get(CourseGetter.BASE_URL + "ssb/searchResults/searchResults",
                                      params=course_params)

        # Parse Course Data

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

            if days and start_time and end_time and reference_number and campus:
                section = Section(
                    code=course_code,
                    reference_number=int(reference_number),
                    campus=campus,
                    days=days,
                    start_time=start_time,
                    end_time=end_time,
                    available_slots=int(available_slots)
                )
                course.add_section(section)

        return course

    @classmethod
    def get_terms(cls) -> "dict(str, str)[]":
        """Fetches and returns the list of available term codes from the Banner system.

        Returns
        ------------
        dict(str, str)
            A dictionary with key as descriptions and value as their term codes
        """
        with requests.Session() as session:
            params = {
                    "offset": 1,
                    "max": 100
            }
            response = session.get(cls.BASE_URL + "ssb/classSearch/getTerms",
                                   params=params)
            term_list = response.json()
            final_dict = {}
            for term in term_list:
                term_code = term.get("code", "")
                term_desc = term.get("description", "")
                if term_code and term_desc:
                    final_dict[term_desc] = term_code
            return final_dict

