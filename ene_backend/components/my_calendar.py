import calendar
from datetime import datetime

import reflex as rx


class VarDate(rx.Base):
    year: int
    month: int
    day: int


class CalendarState(rx.State):
    current_year: int = datetime.now().year
    current_month: int = datetime.now().month
    week_days: list[str] = ["月", "火", "水", "木", "金", "土", "日"]
    dates: list[VarDate] = [
        VarDate(year=base_date.year, month=base_date.month, day=base_date.day)
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
            VarDate(year=base_date.year, month=base_date.month, day=base_date.day)
            for base_date in calendar.Calendar().itermonthdates(self.current_year, self.current_month)
        ]
        self.month = f"{self.current_month}月"


def calendar_view() -> rx.Component:
    def header() -> rx.Component:
        return rx.hstack(
            rx.icon(tag="chevron-left", on_click=CalendarState.prev_month()),
            rx.text(CalendarState.month, justify="center", align="center"),
            rx.icon(tag="chevron-right", on_click=CalendarState.next_month()),
            width="inherit",
            height="auto",
            justify="between",
            # padding="2em 5em",
            _hover={"background": "cyan"},
        )

    def week_days() -> rx.Component:
        return rx.hstack(
            rx.foreach(
                CalendarState.week_days,
                lambda day: rx.box(
                    rx.text(day),
                    text_align="center",
                    width="100%",
                    padding="1em",
                ),
            ),
            width="inherit",
            height="auto",
            justify="between",
            _hover={"background": "cyan"},
        )

    def show_day(var_date: VarDate) -> rx.Component:
        return rx.box(
            rx.text(f"{var_date.day}"),
            justify="start",
            align="start",
            width="100%",
            height="200%",
            padding="0.5em",
            background="white",
            border="1px solid black",
            _hover={"transform": "scale(1.1)"},
        )

    def days() -> rx.Component:
        return rx.grid(
            rx.foreach(CalendarState.dates, show_day),
            columns="7",
            width="inherit",
            height="inherit",
            spacing="0",
            align="end",
            justify="between",
        )

    def render() -> rx.Component:
        return rx.flex(
            header(),
            week_days(),
            days(),
            spacing="0",
            direction="column",
            width="inherit",
            height="inherit",
            padding="1em",
        )

    return render()
