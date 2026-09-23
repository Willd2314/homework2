"""
Homework 2 - Problem 5
William Dellinger

"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from datetime import datetime
from typing import TypeAlias


Observation: TypeAlias = tuple[str, float]
Observations: TypeAlias = dict[str, list[Observation]]
Statistics: TypeAlias = dict[str, tuple[float, float, float]]

DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"


def read_observations(
    filename: str,
) -> tuple[Observations, list[tuple[int, str]]]:
    
    observations_with_dates: dict[str, list[tuple[datetime, str, float]]] = {}
    errors: list[tuple[int, str]] = []
    seen: set[tuple[str, datetime]] = set()

    with open(filename, "r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            if not line:
                errors.append((line_number, "Malformed line: line is empty"))
                continue

            parts = [part.strip() for part in line.split(",")]
            if len(parts) != 3:
                errors.append(
                    (line_number, "Malformed line: expected station,date,temperature")
                )
                continue

            station, date_text, temperature_text = parts

            if not station or not date_text or not temperature_text:
                errors.append(
                    (line_number, "Malformed line: station, date, and temperature are required")
                )
                continue

            try:
                parsed_date = datetime.strptime(date_text, DATE_FORMAT)
            except ValueError:
                errors.append((line_number, f"Invalid date: {date_text}"))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append(
                    (line_number, f"Invalid temperature: {temperature_text}")
                )
                continue

            if not -100.0 <= temperature <= 150.0:
                errors.append(
                    (line_number, f"Temperature out of range: {temperature}")
                )
                continue

            key = (station, parsed_date)
            if key in seen:
                errors.append(
                    (line_number, f"Duplicate observation: {station} at {date_text}")
                )
                continue

            seen.add(key)
            observations_with_dates.setdefault(station, []).append(
                (parsed_date, date_text, temperature)
            )

    observations: Observations = {}

    for station, values in observations_with_dates.items():
        values.sort(key=lambda item: item[0])
        observations[station] = [
            (date_text, temperature)
            for _parsed_date, date_text, temperature in values
        ]

    return observations, errors


def station_statistics(observations: Observations) -> Statistics:
    """Return each station's minimum, maximum, and mean temperature."""
    statistics: Statistics = {}

    for station, values in observations.items():
        if not values:
            continue

        temperatures = [temperature for _date, temperature in values]
        statistics[station] = (
            min(temperatures),
            max(temperatures),
            sum(temperatures) / len(temperatures),
        )

    return statistics


def station_outliers(
    observations: Observations,
) -> dict[str, tuple[str, float, float]]:
    """
    Return stations whose latest temperature is greater than their mean.

    The returned value maps station name to (date, temperature, mean).
    """
    statistics = station_statistics(observations)

    return {
        station: (
            values[-1][0],
            values[-1][1],
            statistics[station][2],
        )
        for station, values in observations.items()
        if values and values[-1][1] > statistics[station][2]
    }


def write_statistics(filename: str, statistics: Statistics) -> None:
    """Write station statistics in lexicographic order with one decimal place."""
    with open(filename, "w", encoding="utf-8") as file:
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            file.write(f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n")


def main() -> None:
    """Read observations from argv, print results, and write statistics."""
    if len(sys.argv) != 3:
        print(
            f"Usage: {os.path.basename(sys.argv[0])} "
            "input_observations.txt output_statistics.txt"
        )
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
        statistics = station_statistics(observations)
        outliers = station_outliers(observations)

        print("William Dellinger")
        print("\nStatistics:")
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            print(
                f"{station}: min={minimum:.1f}, "
                f"max={maximum:.1f}, mean={mean:.1f}"
            )

        print("\nOutliers:")
        for station in sorted(outliers):
            date, temperature, mean = outliers[station]
            print(
                f"{station}: date={date}, "
                f"temperature={temperature:.1f}, mean={mean:.1f}"
            )

        print("\nErrors:")
        if errors:
            for line_number, message in errors:
                print(f"Line {line_number}: {message}")
        else:
            print("None")

        write_statistics(output_filename, statistics)
        print(f"\nStatistics written to {output_filename}")

    except (OSError, IOError) as exc:
        print(f"File access error: {exc}")


class TestWeatherStationAnalyzer(unittest.TestCase):
    """Unit tests for the weather station analyzer."""

    def make_file(self, content: str) -> str:
        """Create and return a temporary text file containing content."""
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
        )
        handle.write(content)
        handle.close()
        self.addCleanup(
            lambda: os.path.exists(handle.name) and os.remove(handle.name)
        )
        return handle.name

    def test_several_stations(self) -> None:
        filename = self.make_file(
            "A,09:00:00 AM 04/20/2026,70\n"
            "B,10:00:00 AM 04/20/2026,80\n"
        )
        observations, errors = read_observations(filename)
        self.assertEqual(set(observations), {"A", "B"})
        self.assertEqual(errors, [])

    def test_negative_temperature(self) -> None:
        filename = self.make_file(
            "A,09:00:00 AM 04/20/2026,-12.5\n"
        )
        observations, errors = read_observations(filename)
        self.assertEqual(observations["A"][0][1], -12.5)
        self.assertEqual(errors, [])

    def test_duplicate_observation(self) -> None:
        filename = self.make_file(
            "A,09:00:00 AM 04/20/2026,70\n"
            "A,09:00:00 AM 04/20/2026,71\n"
        )
        observations, errors = read_observations(filename)
        self.assertEqual(len(observations["A"]), 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("Duplicate", errors[0][1])

    def test_invalid_range(self) -> None:
        filename = self.make_file(
            "A,09:00:00 AM 04/20/2026,151\n"
            "B,09:00:00 AM 04/20/2026,-101\n"
        )
        observations, errors = read_observations(filename)
        self.assertEqual(observations, {})
        self.assertEqual(len(errors), 2)

    def test_calculated_statistics(self) -> None:
        observations = {
            "A": [
                ("09:00:00 AM 04/20/2026", 10.0),
                ("10:00:00 AM 04/20/2026", 20.0),
                ("11:00:00 AM 04/20/2026", 30.0),
            ]
        }
        stats = station_statistics(observations)
        self.assertEqual(stats["A"], (10.0, 30.0, 20.0))

    def test_sorted_output(self) -> None:
        stats = {
            "Zulu": (1.0, 3.0, 2.0),
            "Alpha": (10.0, 30.0, 20.0),
        }
        output = self.make_file("")
        write_statistics(output, stats)

        with open(output, "r", encoding="utf-8") as file:
            lines = file.readlines()

        self.assertTrue(lines[0].startswith("Alpha,"))
        self.assertTrue(lines[1].startswith("Zulu,"))
        self.assertIn(",10.0,30.0,20.0", lines[0])

    def test_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_observations("this_file_should_not_exist_987654.txt")

    def test_outliers(self) -> None:
        observations = {
            "A": [
                ("09:00:00 AM 04/20/2026", 50.0),
                ("10:00:00 AM 04/20/2026", 70.0),
            ],
            "B": [
                ("09:00:00 AM 04/20/2026", 80.0),
                ("10:00:00 AM 04/20/2026", 70.0),
            ],
        }
        outliers = station_outliers(observations)
        self.assertIn("A", outliers)
        self.assertNotIn("B", outliers)

    def test_observations_sorted_by_datetime(self) -> None:
        filename = self.make_file(
            "A,11:00:00 AM 04/20/2026,80\n"
            "A,09:00:00 AM 04/20/2026,60\n"
            "A,10:00:00 AM 04/20/2026,70\n"
        )
        observations, errors = read_observations(filename)
        self.assertEqual(errors, [])
        self.assertEqual(
            [date for date, _temperature in observations["A"]],
            [
                "09:00:00 AM 04/20/2026",
                "10:00:00 AM 04/20/2026",
                "11:00:00 AM 04/20/2026",
            ],
        )


if __name__ == "__main__":
    main()
