import streamlit
import pandas as pd
import sys
import requests
import time
from get_course import CourseGetter
from get_schedules import ScheduleGetter

streamlit.title("Course Schedule Generator")
term = streamlit.text_input("Enter Term (e.g., '202630'):")
course_codes_input = streamlit.text_input("Enter Course Codes (comma-separated):")
course_codes = [code.strip() for code in course_codes_input.split(",") if 
                    code.strip()]

if streamlit.button("Generate Schedules") and term and course_codes:
    with requests.Session() as session:
        # Set courses
        course_getter = CourseGetter(session, term)

        courses = []
        for code in course_codes:
            course = course_getter.get_course(code)
            courses.append(course)

        # Generate schedules
        schedule_getter = ScheduleGetter(courses)
        schedules = schedule_getter.make_schedules()

        streamlit.write(f"Generated {len(schedules)} possible schedules:")

        for i, schedule in enumerate(schedules):
            streamlit.write(f"### Schedule {i + 1}")
            data = {
                "CRN": [section.reference_number for section in schedule],
                "Days": [", ".join([day.value.upper() for day in section.days]) 
                            for section in schedule],
                "Start Time": [time.strftime("%H:%M",section.start_time) for section
                                    in schedule],
                "End Time": [time.strftime("%H:%M",section.end_time) for section 
                                in schedule],
                "Campus": [section.campus for section in schedule],
                "Available Slots": [section.available_slots for section in
                    schedule],
            }
            df = pd.DataFrame(data, index=[section.code for section in schedule])
            streamlit.dataframe(df)
