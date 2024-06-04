"""Reflex custom component Calendar."""

# For wrapping react guide, visit https://reflex.dev/docs/wrapping-react/overview/

from datetime import datetime
from typing import Any, Literal

import reflex as rx
from reflex.utils import format, imports

LiteralCalendarType = Literal["gregory", "hebrew", "islamic", "iso8601"]
LiteralDefaultView = Literal["month", "year", "decade", "century"]
LiteralReturnValue = Literal["start", "end", "range"]


class Calendar(rx.Component):
    """Calendar component."""

    library = "react-calendar@4.8.0"
    tag = "Calendar"
    is_default = True
    alias = "ReflexCalendar"
    active_start_date: rx.Var[datetime]
    active_end_date: rx.Var[datetime]
    allow_partial_range: rx.Var[bool]
    calendar_type: rx.Var[LiteralCalendarType]
    default_value: rx.Var[str]
    default_view: rx.Var[LiteralDefaultView] = "month"
    go_to_range_start_on_select: rx.Var[bool]
    locale: rx.Var[str]
    max_date: rx.Var[str]
    max_detail: rx.Var[LiteralDefaultView]
    min_date: rx.Var[str]
    min_detail: rx.Var[LiteralDefaultView]
    navigation_aria_label: rx.Var[str]
    navigation_aria_live: rx.Var[str]
    navigation_label: rx.Var[str]
    next_2_aria_label: rx.Var[str]
    next_2_label: rx.Var[str]
    next_aria_label: rx.Var[str]
    next_label: rx.Var[str]
    prev_2_aria_label: rx.Var[str]
    prev_2_label: rx.Var[str]
    prev_aria_label: rx.Var[str]
    prev_label: rx.Var[str]
    return_value: rx.Var[LiteralReturnValue]
    select_range: rx.Var[bool]
    show_double_view: rx.Var[bool]
    show_fixed_number_of_weeks: rx.Var[bool]
    show_navigation: rx.Var[bool]
    show_neighouring_century: rx.Var[bool]
    show_neighbouring_decade: rx.Var[bool]
    show_neighbouring_month: rx.Var[bool]
    show_week_numbers: rx.Var[bool]
    value: rx.Var[str]
    view: rx.Var[LiteralDefaultView]

    def _get_imports(self) -> imports.ImportDict:
        return imports.merge_imports(
            super()._get_imports(),
            {
                "": {imports.ImportVar(tag=f"{format.format_library_name(self.library)}/dist/Calendar.css")},
            },
        )

    @classmethod
    def create(cls, *children, **props) -> "Calendar":
        """Create a Calendar component."""
        style = props.pop("style", {})
        style["color"] = props.pop("color", rx.color("accent", 11))
        style["background_color"] = props.pop("background_color", rx.color("accent", 1))
        props["style"] = style

        return cls(*children, **props)

    def get_event_triggers(self) -> dict[str, Any]:
        return {
            **super().get_event_triggers(),
            "on_active_start_date_change": lambda e0: [
                rx.Var.create(f"{{...{e0}, activeStartDate: {e0}.activeStartDate.toDateString()}}")
            ],
            "on_change": lambda date: [rx.Var.create(f"{date}.toDateString()")],
            "on_click_day": lambda date: [rx.Var.create(f"{date}.getDate()")],
            "on_click_month": lambda date: [rx.Var.create(f"{date}.getMonth()+1")],
            "on_click_week_number": lambda date: [rx.Var.create(f"{date}.getDay()")],
            "on_click_year": lambda date: [rx.Var.create(f"{date}.getFullYear()")],
            "on_click_decade": lambda date: [rx.Var.create(f"{date}.getFullYear()")],
            "on_drill_down": lambda e0: [rx.Var.create(f"{e0}.view")],
            "on_drill_up": lambda e0: [rx.Var.create(f"{e0}.view")],
            "on_view_change": lambda e0: [e0],  # use on_view_change for full event
        }


calendar = Calendar.create


def reformat_date(date: str, output_format: str = "%Y-%m-%d") -> datetime:
    """Reformat a date."""
    return datetime.strptime(date, "%a %b %d %Y").strftime(output_format)
