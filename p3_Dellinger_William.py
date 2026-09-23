"""
Homework 2 - Problem 3
William Dellinger
"""

from __future__ import annotations

import csv


SocialNetwork = dict[str, tuple[str, list[str]]]


def add_user(sn: SocialNetwork, username: str, fullname: str) -> bool:
    try:
        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True
    except Exception as exc:
        print(f"Unable to add user '{username}': {exc}")
        raise


def add_friend(sn: SocialNetwork, user1: str, user2: str) -> bool:
    try:
        if user1 not in sn or user2 not in sn or user1 == user2:
            return False

        friends1 = sn[user1][1]
        friends2 = sn[user2][1]

        if user2 not in friends1:
            friends1.append(user2)
        if user1 not in friends2:
            friends2.append(user1)

        return True
    except Exception as exc:
        print(f"Unable to add friendship between '{user1}' and '{user2}': {exc}")
        raise


def get_friends(sn: SocialNetwork, user1: str, distance: int) -> list[str]:
    try:
        if user1 not in sn or distance <= 0:
            return []

        visited = {user1}
        frontier = [user1]
        result: list[str] = []

        for _ in range(distance):
            next_frontier: list[str] = []

            for username in frontier:
                for friend in sn[username][1]:
                    if friend not in visited:
                        visited.add(friend)
                        result.append(friend)
                        next_frontier.append(friend)

            if not next_frontier:
                break

            frontier = next_frontier

        return result
    except Exception as exc:
        print(f"Unable to get friends for '{user1}': {exc}")
        raise


def save_network(filename: str, sn: SocialNetwork) -> None:
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname, *friends])
    except Exception as exc:
        print(f"Unable to save network to '{filename}': {exc}")
        raise


def load_network(filename: str) -> SocialNetwork:
    try:
        sn: SocialNetwork = {}

        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:
                    continue
                username = row[0]
                fullname = row[1]
                friends = row[2:]
                sn[username] = (fullname, friends)

        return sn
    except Exception as exc:
        print(f"Unable to load network from '{filename}': {exc}")
        raise


def main() -> None:
    print("William Dellinger")

    sn: SocialNetwork = {
        "alice": ("Alice Smith", ["maria"]),
        "maria": ("Maria Cortez", ["alice", "joe", "david"]),
        "joe": ("Joseph Adams", ["maria", "eve"]),
        "eve": ("Evelyn Cooper", ["joe"]),
        "david": ("David Benson", ["maria"]),
    }

    print("\nInitial network:")
    print(sn)

    print("\nAdd user:")
    print("Adding sam:", add_user(sn, "sam", "Sam Wilson"))
    print("Adding alice again:", add_user(sn, "alice", "Alice Smith"))

    print("\nAdd friend:")
    print("Link sam/eve:", add_friend(sn, "sam", "eve"))
    print("Link unknown/eve:", add_friend(sn, "unknown", "eve"))

    print("\nFriends:")
    print("alice distance 1:", get_friends(sn, "alice", 1))
    print("alice distance 2:", get_friends(sn, "alice", 2))
    print("alice distance 3:", get_friends(sn, "alice", 3))
    print("unknown distance 2:", get_friends(sn, "unknown", 2))

    filename = "social_network.csv"
    save_network(filename, sn)
    print(f"\nSaved network to {filename}")

    loaded = load_network(filename)
    print("Loaded network:")
    print(loaded)


if __name__ == "__main__":
    main()
