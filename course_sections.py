import time
import enum

class Days(enum.Enum):
    """Enumeration for days of the week."""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Section:
    """Represents a section of a course, containing scheduling and enrollment 
    details.
    
    Params
    --------------
    reference_number : int
        The unique reference number for this section.
    days : Days[]
        The days of the week when this section meets.
    start_time : str
        The start time of the section in HHMM format, e.g., "1300" for 1:00 PM.
    end_time : str
        The end time of the section in HHMM format, e.g., "1450" for 2:50 PM.
    available_slots : int
        The number of available enrollment slots left in this section.
    """

    def __init__(self, reference_number: int, days: "Days[]", 
                 start_time: str, end_time: str, available_slots: int):
        self._reference_number = reference_number
        self._days = days
        self._available_slots = available_slots

        formatted_start_time = start_time[:2] + ":" + start_time[2:]
        formatted_end_time = end_time[:2] + ":" + end_time[2:]
        self._start_time = time.strptime(formatted_start_time, "%H:%M")
        self._end_time = time.strptime(formatted_end_time, "%H:%M")

    @property
    def reference_number(self) -> int:
        return self._reference_number

    @property
    def days(self) -> "str[]":
        return self._days

    @property
    def start_time(self) -> time:
        return self._start_time

    @property
    def end_time(self) -> time:
        return self._end_time

    @property
    def available_slots(self) -> int:
        return self._available_slots

    def __str__(self) -> str:
        days_str = ', '.join([day.name for day in self.days])
        return (f"Section {self.reference_number}: "
                f"{days_str} from {time.strftime('%H:%M', self.start_time)} "
                f"to {time.strftime('%H:%M', self.end_time)} - "
                f"Available Slots: {self.available_slots}")

class Course:
    """Represents a collection of sections for a specific course, which can be
    iterated over."""

    def __init__(self, code: str):
        self._code = code
        self._sections = []

    def add_section(self, section: Section):
        """Adds a section to the collection if it matches the course code."""
        if not isinstance(section, Section):
            raise TypeError("Expected a Section instance")

        self._sections.append(section)

    @property
    def code(self) -> str:
        return self._code

    @property
    def sections(self):
        return self._sections

    def __iter__(self):
        """Returns an iterator over the sections."""
        return iter(self.sections)




