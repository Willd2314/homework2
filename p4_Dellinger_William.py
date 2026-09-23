"""
Homework 2 - Problem 4
William Dellinger
"""

from __future__ import annotations

import csv
from collections import defaultdict


def load_ranked_movies(filename: str) -> set[tuple[str, str]]:
    movies: set[tuple[str, str]] = set()

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movies.add((row["Title"], row["Year"]))

    return movies


def load_casts(
    filename: str,
) -> list[tuple[str, str, str, list[str]]]:
    records: list[tuple[str, str, str, list[str]]] = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 4:
                continue

            title = row[0]
            year = row[1]
            director = row[2]
            actors = [actor for actor in row[3:] if actor.strip()]
            records.append((title, year, director, actors))

    return records


def load_grossing_movies(filename: str) -> dict[tuple[str, str], float]:
    movies: dict[tuple[str, str], float] = {}

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            amount_text = row["USA Box Office"]
            cleaned = amount_text.replace("$", "").replace(",", "").strip()
            movies[(row["Title"], row["Year"])] = float(cleaned)

    return movies


def display_top_collaborations(
    top_rated_filename: str,
    casts_filename: str,
    limit: int | None = None,
) -> list[tuple[str, str, int]]:
    top_rated = load_ranked_movies(top_rated_filename)
    casts = load_casts(casts_filename)

    counts: dict[tuple[str, str], int] = defaultdict(int)

    for title, year, director, actors in casts:
        if (title, year) in top_rated:
            for actor in actors:
                counts[(director, actor)] += 1

    ranking = [
        (director, actor, count)
        for (director, actor), count in counts.items()
    ]
    ranking.sort(key=lambda item: item[2], reverse=True)

    shown = ranking if limit is None else ranking[:limit]

    print("\nTop Director/Actor Collaborations")
    for rank, item in enumerate(shown, start=1):
        director, actor, count = item
        print(f"{rank:2}. {director} / {actor}: {count}")

    return ranking


def display_top_actors(
    top_grossing_filename: str,
    casts_filename: str,
    limit: int | None = None,
) -> list[tuple[str, float]]:
    
    grossing = load_grossing_movies(top_grossing_filename)
    casts = load_casts(casts_filename)

    totals: dict[str, float] = defaultdict(float)

    for title, year, _director, actors in casts:
        movie_key = (title, year)
        if movie_key in grossing:
            for actor in actors:
                totals[actor] += grossing[movie_key]

    ranking = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    shown = ranking if limit is None else ranking[:limit]

    print("\nTop Actors by Total USA Box Office")
    for rank, (actor, total) in enumerate(shown, start=1):
        print(f"{rank:2}. {actor}: ${total:,.0f}")

    return ranking


def main() -> None:
    print("William Dellinger")

    top_rated_file = "imdb-top-rated.csv"
    top_grossing_file = "imdb-top-grossing.csv"
    casts_file = "imdb-top-casts.csv"

    try:
        display_top_collaborations(top_rated_file, casts_file, limit=10)
        display_top_actors(top_grossing_file, casts_file, limit=10)
    except FileNotFoundError as exc:
        print(
            "\nCSV file not found. Put imdb-top-rated.csv, "
            "imdb-top-grossing.csv, and imdb-top-casts.csv "
            "in the same folder as this program."
        )
        print(exc)


if __name__ == "__main__":
    main()
