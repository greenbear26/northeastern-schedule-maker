class ScheduleGetter:
    """Generates all possible non-conflicting schedules from a list of
    courses. Will take in parameters for filtering courses in the future.

    Params
    ------------
    courses : Course[]
        A list of Course objects to generate schedules from.
    """

    def __init__(self, courses: "Course[]"):
        self._courses = courses

    @staticmethod
    def _is_valid(section) -> bool:
        return section.available_slots > 0

    @staticmethod
    def _is_conflict(new_section, current_section) -> bool:
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

    def _backtrack(self, all_schedules, current_schedule, course_index):
        # Base case: all courses have been scheduled
        if course_index == len(self._courses):
            if len(current_schedule) == len(self._courses):
                all_schedules.append(current_schedule.copy())
            return

        # Try to schedule each section of the current course
        for section in self._courses[course_index]:
            # Check if section is valid
            if not ScheduleGetter._is_valid(section):
                continue

            # Check for conflicts with already scheduled sections
            conflict = False
            for scheduled_section in current_schedule:
                if ScheduleGetter._is_conflict(section, scheduled_section):
                    conflict = True
                    break

            # If no conflict, add section to schedule and recurse
            if not conflict:
                current_schedule.append(section)
                self._backtrack(all_schedules, current_schedule, course_index + 1)
                current_schedule.pop()

    def make_schedules(self) -> "Section[]":
        """Generates all possible non-conflicting schedules from the provided courses.

        Params
        ------------
        courses : Course[]
            A list of Course objects to generate schedules from.

        Returns
        ------------
        Course[][]
            A list of possible schedules, where each schedule is a list of Section
            objects.
        """

        all_schedules = []
        self._backtrack(all_schedules, [], 0)
        return all_schedules
