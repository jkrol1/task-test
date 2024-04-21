from command.grep import Grep

if __name__ == "__main__":
    Grep(
        "super interesting data x2",
        ["*.txt", "../*.py", "*"],
        recursive=False
    ).execute()
