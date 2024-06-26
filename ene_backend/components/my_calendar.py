import calendar
from datetime import datetime

import reflex as rx


class VarDate(rx.Base):
    year: int
    month: int
    day: int
    weekday: int


class CalendarState(rx.State):
    current_year: int = datetime.now().year
    current_month: int = datetime.now().month
    current_day: int = datetime.now().day
    week_days: list[str] = ["月", "火", "水", "木", "金", "土", "日"]
    dates: list[VarDate] = [
        VarDate(
            year=base_date.year,
            month=base_date.month,
            day=base_date.day,
            weekday=base_date.weekday(),
        )
        for base_date in calendar.Calendar().itermonthdates(current_year, current_month)
    ]
    month: str = f"{current_month}月"

    def next_month(self) -> None:
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

    def prev_month(self) -> None:
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def update_calendar(self) -> None:
        self.dates = [
            VarDate(year=base_date.year, month=base_date.month, day=base_date.day, weekday=base_date.weekday())
            for base_date in calendar.Calendar().itermonthdates(self.current_year, self.current_month)
        ]
        self.month = f"{self.current_month}月"


def calendar_view() -> rx.Component:
    def header() -> rx.Component:
        return rx.hstack(
            rx.icon(tag="chevron-left", on_click=CalendarState.prev_month()),
            rx.text(CalendarState.month, justify="center", align="center"),
            rx.icon(tag="chevron-right", on_click=CalendarState.next_month()),
            width="100%",
            justify="between",
            align="start",
        )

    def week_days() -> rx.Component:
        return rx.hstack(
            rx.foreach(
                CalendarState.week_days,
                lambda day: rx.box(
                    rx.text(day),
                    text_align="center",
                    width="100%",
                ),
            ),
            width="100%",
            justify="between",
            align="start",
        )

    def show_day(var_date: VarDate) -> rx.Component:
        return rx.box(
            rx.text(
                f"{var_date.day}",
                color=rx.color_mode_cond(
                    rx.cond(
                        var_date.day == CalendarState.current_day,
                        "darkorange",
                        rx.cond(
                            ~(var_date.month == CalendarState.current_month),
                            "gray",
                            rx.cond(var_date.weekday == 5, "blue", rx.cond(var_date.weekday == 6, "red", "#333333")),
                        ),
                    ),
                    rx.cond(
                        var_date.day == CalendarState.current_day,
                        "yellow",
                        rx.cond(
                            ~(var_date.month == CalendarState.current_month),
                            "gray",
                            rx.cond(
                                var_date.weekday == 5, "#AAAAFF", rx.cond(var_date.weekday == 6, "#FFAAAA", "white")
                            ),
                        ),
                    ),
                ),
            ),
            width="100%",
            height="100%",
            padding="0.5em",
            background=rx.color_mode_cond("white", "#333333"),
            border=rx.color_mode_cond("1px solid black", "1px solid white"),
            _hover={"transform": "scale(1.1)"},
        )

    def days() -> rx.Component:
        return rx.grid(
            rx.foreach(CalendarState.dates, show_day),
            columns="7",
            flow="row-dense",
            width="100%",
            height="100%",
            spacing="0",
        )

    def render() -> rx.Component:
        return rx.flex(
            header(),
            week_days(),
            days(),
            spacing="0",
            direction="column",
            width="100%",
            height="100%",
            max_height="100%",
            padding="1em",
            align="start",
            justify="start",
            sizing="border-box",
        )

    return render()
