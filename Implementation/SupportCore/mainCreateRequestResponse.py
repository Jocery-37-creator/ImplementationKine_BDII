# main.py

from create_request import create_request
from create_response import create_response


def main():
    print("1. Create Request")
    print("2. Add Response a Request")

    opcion = input("Choose one option: ").strip()

    if opcion == "1":
        create_request()
    elif opcion == "2":
        create_response()
    else:
        print("Option invalid.")


if __name__ == "__main__":
    main()
