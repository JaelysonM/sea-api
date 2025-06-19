from datetime import datetime, timedelta, date
from ortools.sat.python import cp_model
import random


class Scheduler:
    def __init__(
        self,
        work_start: str,
        work_end: str,
        min_price: float,
        max_price: float,
        max_parallel: int = 2,
        buffer_time: int = 60,
        avg_threshold: float = 0.1,
    ):
        self.work_start = work_start
        self.work_end = work_end
        self.min_price = min_price
        self.max_price = max_price
        self.max_parallel = max_parallel
        self.buffer_time = buffer_time
        self.avg_threshold = avg_threshold
        self.appointments = []

    def time_to_minutes(self, time: str) -> int:
        parts = list(map(int, time.split(":")))
        if len(parts) == 3:
            h, m, s = parts
        else:
            h, m = parts
        return h * 60 + m

    def minutes_to_time(self, minutes: int) -> str:
        if minutes is None:
            return None
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    def add_appointment(
        self, date: str, start: str, duration: int
    ):
        start_min = self.time_to_minutes(start)
        end_min = start_min + duration
        end = self.minutes_to_time(end_min)
        self.appointments.append((date, start, end))

    def get_appointments(self, date: str):
        return [
            (start, end)
            for d, start, end in self.appointments
            if d == date
        ]

    def count_overlapping_appointments(
        self, candidate_start: str, candidate_end: str
    ) -> int:
        cand_start = self.time_to_minutes(candidate_start)
        cand_end = self.time_to_minutes(candidate_end)
        count = 0
        for d, start, end in self.appointments:
            s = self.time_to_minutes(start)
            e = self.time_to_minutes(end)
            if not (e <= cand_start or s >= cand_end):
                count += 1
        return count

    def filter_candidates(
        self,
        appointments: list,
        duration: int,
        max_parallel: int,
        start: str,
        end: str,
    ) -> list:
        start_min = self.time_to_minutes(start)
        end_min = self.time_to_minutes(end)
        total_min = end_min - start_min
        timeline = [0] * total_min
        for appt_start, appt_end in appointments:
            appt_start_min = self.time_to_minutes(
                appt_start
            )
            appt_end_min = self.time_to_minutes(appt_end)
            for i in range(
                max(0, appt_start_min - start_min),
                min(total_min, appt_end_min - start_min),
            ):
                timeline[i] += 1
        candidates = []
        for candidate in range(
            start_min, end_min - duration + 1
        ):
            if candidate % 10 != 0:
                continue
            if all(
                timeline[i] < max_parallel
                for i in range(
                    candidate - start_min,
                    candidate - start_min + duration,
                )
            ):
                candidates.append(candidate)
        return candidates

    def optimize_schedule(
        self, candidates: list, duration: int, now: str
    ):
        now_min = self.time_to_minutes(now)
        lower_bound = now_min + self.buffer_time
        model = cp_model.CpModel()
        if not candidates:
            return None
        candidate_var = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(candidates),
            "candidate",
        )
        model.Add(candidate_var >= lower_bound)
        model.Minimize(candidate_var)
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        return (
            solver.Value(candidate_var)
            if status
            in (cp_model.OPTIMAL, cp_model.FEASIBLE)
            else None
        )

    def nice_price(self, price: float) -> float:
        price = min(price, self.max_price)
        base = int(price)
        candidate1 = base + 0.49
        candidate2 = base + 0.90
        if candidate1 > self.max_price:
            candidate1 = self.max_price
        if candidate2 > self.max_price:
            candidate2 = self.max_price
        return (
            candidate1
            if abs(price - candidate1)
            <= abs(price - candidate2)
            else candidate2
        )

    def suggest_price(
        self,
        candidate_min: int,
        duration: int,
        avg_count: float,
    ) -> float:
        candidate_start = self.minutes_to_time(
            candidate_min
        )
        candidate_end = self.minutes_to_time(
            candidate_min + duration
        )
        count = self.count_overlapping_appointments(
            candidate_start, candidate_end
        )
        if count >= avg_count * (1 + self.avg_threshold):
            price = self.max_price
        else:
            ratio = (
                count
                / (avg_count * (1 + self.avg_threshold))
                if avg_count > 0
                else 0
            )
            price = (
                self.min_price
                + (self.max_price - self.min_price) * ratio
            )
        return self.nice_price(round(price, 2))

    def suggest_schedule(
        self, date: date, duration: int, now: datetime
    ):
        now_time = now.strftime("%H:%M")
        now_date = now.date()
        if date < now_date:
            return (None, [])
        appointments = self.get_appointments(str(date))
        candidates = self.filter_candidates(
            appointments,
            duration,
            self.max_parallel,
            self.work_start,
            self.work_end,
        )
        now_min = self.time_to_minutes(now_time)
        lower_bound = (
            now_min + self.buffer_time
            if date == now_date
            else self.time_to_minutes(self.work_start)
        )
        if date == now_date:
            candidates = [
                c for c in candidates if c >= lower_bound
            ]
        if not candidates:
            return (None, [])
        counts = [
            self.count_overlapping_appointments(
                self.minutes_to_time(c),
                self.minutes_to_time(c + duration),
            )
            for c in candidates
        ]
        avg_count = (
            sum(counts) / len(counts) if counts else 0
        )
        available_slots = [
            {
                "time": self.minutes_to_time(c),
                "price": self.suggest_price(
                    c, duration, avg_count
                ),
            }
            for c in candidates
        ]
        if date == now_date:
            best = self.optimize_schedule(
                candidates, duration, now_time
            )
        else:
            best = min(candidates)
        return (self.minutes_to_time(best), available_slots)
