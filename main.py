import streamlit
from streamlit_calendar import calendar
import pandas as pd
import sys
import requests
import time
from course_sections import Days
from get_course import CourseGetter
from get_schedules import ScheduleGetter
from time import sleep

DAYS_TO_DATE = {
    Days.MON: "2025-12-22",
    Days.TUE: "2025-12-23",
    Days.WED: "2025-12-24",
    Days.THU: "2025-12-25",
    Days.FRI: "2025-12-26",
}

CALENDAR_OPTIONS = {
    "initialView": "timeGridFiveDay",
    "initialDate": "2025-12-22",
    "weekends": False,
    "dayHeaderFormat": { "weekday": "short" },
    "firstDay": 1,
    "headerToolbar": False,
    "dayHeaders": False,
    "slotMinTime": "08:00:00",
    "slotMaxTime": "22:00:00",
    "slotDuration": "01:00:00",  # Duration of each slot
    "slotLabelInterval": "01:00:00",  # Label every hour
    "slotLabelStepSize": "01:00",  # Step size for labels
    "views": {
      "timeGridFiveDay": {
        "type": "timeGrid",
        "dayCount": 5,
        "buttonText": "Week"
      }
    },
    "height": 600,
}

CALENDAR_CSS = """
    .fc-col-time-frame {
        height: auto !important;
    }
    .fc-timegrid-slot {
        height: 6em !important;  /* Increase from default ~2em */
    }
    .fc-event-title {
        font-size: 10px;
        font-weight: 700;
        word-wrap: break-word;
        white-space: pre-wrap;
        line-height: 1.3;
    }
    .fc-event {
        overflow: auto;
        max-height: 120px;
        padding: 4px;
    }
"""

def construct_calender_events(schedules: "Section[][]"):
    streamlit.session_state.calendar_events = []
    
    for schedule in schedules:
        events = []
        for section in schedule:
            for day in section.days:
                date = DAYS_TO_DATE[day]
                start_time = time.strftime("%H:%M:%S", section.start_time)
                end_time = time.strftime("%H:%M:%S", section.end_time)
                event = {
                    "start": f"{date}T{start_time}",
                    "end": f"{date}T{end_time}",
                    "title": f"Course:{section.code}\n"
                        f"CRN:{section.reference_number}\n"
                        f"Campus:{section.campus}\n"
                        f"Teacher:{section.instructor}"
                }
                events.append(event)
        streamlit.session_state.calendar_events.append(events)
    




streamlit.title(":red[NEU Course Schedule Generator]")

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
        course_getter = CourseGetter(session, term)

        with streamlit.spinner("Fetching course data..."):
            courses = []
            for code in course_codes:
                course = course_getter.get_course(code)
                courses.append(course)

    # Generate schedules
    schedule_getter = ScheduleGetter(courses)
    schedules = schedule_getter.make_schedules()

    
    # Construct events AFTER generating schedules
    construct_calender_events(schedules)

# Display calendars (this runs on every rerun, but uses session_state)
if 'calendar_events' in streamlit.session_state:
    streamlit.write(f"Generated {len(streamlit.session_state.calendar_events)} possible schedules:")
    for i, events in enumerate(streamlit.session_state.calendar_events):
        streamlit.write(f"### Schedule {i + 1}")
        calendar(
            key=f"course_schedule_calendar_{i+1}",
            events=events,  # Pass events directly (not a nested list)
            options=CALENDAR_OPTIONS,
            custom_css=CALENDAR_CSS
        )

