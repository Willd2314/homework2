import ast


def line_number(input_file: str, output_file: str) -> None:
    try:
        with open(input_file, "r") as infile:
            with open(output_file, "w") as outfile:
                for number, line in enumerate(infile, start=1):
                    outfile.write(f"{number}. {line}")

    except Exception as error:
        print("There was a problem reading or writing the file.")
        raise 


def parse_functions(filename: str) -> tuple:
    try:
        with open(filename, "r") as file:
            code = file.read()

        tree = ast.parse(code)
        lines = code.splitlines()

        functions = []

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                line_num = node.lineno
                name = node.name
                arguments = ast.unparse(node.args)

                function_lines = lines[node.lineno - 1:node.end_lineno]

                cleaned_lines = []

                for line in function_lines:
                    if line.strip() != "" and not line.strip().startswith("#"):
                        cleaned_lines.append(line)

                function_code = "\n".join(cleaned_lines)

                functions.append(
                    (line_num, name, arguments, function_code)
                )

        functions.sort(key=lambda function: function[1])

        return tuple(functions)

    except Exception as error:
        print("There was a problem parsing the Python file.")
        raise error


def main() -> None:
    """Test the functions using this Python file."""
    print("William Dellinger")

    filename = "p1_Dellinger_William.py"
    output_file = "p1_Dellinger_William.py.txt"

    line_number(filename, output_file)

    print(f"\nCreated numbered file: {output_file}")

    print("\nParsed functions:")

    functions = parse_functions(filename)

    for function in functions:
        print(function)


if __name__ == "__main__":
    main()