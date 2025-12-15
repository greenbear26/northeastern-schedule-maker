from abc import Iterable
from section import Section
from datetime import time
import enum

class Course:
    """Represents a course with a subject and name."""

    def __init__(self, subject: str, name: str):
        self._subject = subject
        self._name = name

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def name(self) -> str:
        return self._name

class Section:
    """Represents a section of a course, containing scheduling and enrollment 
    details."""

    def __init__(self, course: Course, days: str[], start_time: time, end_time: time, 
                 filled_slots: int, total_slots: int):
        self._course = course
        self._days = days
        self._start_time = start_time
        self._end_time = end_time
        self._filled_slots = filled_slots
        self._total_slots = total_slots

    @property
    def course(self) -> Course:
        return self._course

    @property
    def days(self) -> str[]:
        return self._days

    @property
    def start_time(self) -> time:
        return self._start_time

    @property
    def end_time(self) -> time:
        return self._end_time

    @property
    def filled_slots(self) -> int:
        return self._filled_slots

    @property
    def total_slots(self) -> int:
        return self._total_slots


class CourseSections(Iterable):
    """Represents a collection of sections for a specific course code."""

    def __init__(self, code: str):
        self._code = code
        self._sections = []

    def add_section(self, section: Section):
        """Adds a section to the collection if it matches the course code."""
        if not isinstance(section, Section):
            raise TypeError("Expected a Section instance")

        if section.code != self.code:
            raise ValueError("Section code does not match CourseSections code")
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

