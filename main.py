import streamlit
import pandas as pd
import sys
import requests
import time
from get_course import CourseGetter
from get_schedules import ScheduleGetter

streamlit.title("Course Schedule Generator")

term_dict = CourseGetter.get_terms()
term_description = streamlit.selectbox("Select Term", term_dict.keys())

course_df = pd.DataFrame({
    'Course Codes': ['']
})
course_codes_input = streamlit.data_editor(course_df, num_rows="dynamic",
                                           hide_index=True)

if streamlit.button("Generate Schedules"):
    term = term_dict[term_description]
    course_codes = [course.strip() for course in course_codes_input['Course Codes'].tolist()
                if course is not None and course.strip() != '']

    if not course_codes:
        streamlit.error("Please enter at least one course code.")
        sys.exit(1)

    if not term:
        streamlit.error("Please select a valid term.")
        sys.exit(1)

    with requests.Session() as session:
        # Set courses
        course_getter = CourseGetter(session, term)

        with streamlit.spinner("Fetching course data..."):
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
            streamlit.dataframe(df, hide_index=True)
