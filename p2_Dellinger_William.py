"""
Homework 2 - Problem 2
William Dellinger
"""


def main() -> None:
    print("William Dellinger")

    # a)
    equal_sums = [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if len({a, b, c, d}) == 4 and a * a + b * b == c * c + d * d
    ]
    print("\na)", equal_sums)

    # b)
    words = ["One", "SEVEN", "three", "two", "Ten"]
    short_words = [(word.lower(), len(word)) for word in words if len(word) < 5]
    print("\nb)", short_words)

    # c)
    names = ["Christopher Ashton Kutcher", "Elizabeth Stamatina Fey"]
    abbreviated_names = [
        f"{parts[0]} {parts[1][0]}. {parts[2]}"
        for name in names
        for parts in [name.split()]
    ]
    print("\nc)", abbreviated_names)

    # d)
    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
    anagrams = [
        (w1, w2)
        for w1 in lst1
        for w2 in lst2
        if sorted(w1.lower()) == sorted(w2.lower())
    ]
    print("\nd)", anagrams)

    # e)
    s = ["one", "two", "three"]
    lengths = {word: len(word) for word in s}
    print("\ne)", lengths)

    # f)
    text = "Hello world"
    vowel_positions = {
        index: char
        for index, char in enumerate(text)
        if char.lower() in "aeiou"
    }
    print("\nf)", vowel_positions)


if __name__ == "__main__":
    main()
