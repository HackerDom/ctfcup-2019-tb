from command_parser import parse
from controller import MethodController


def main():
    method_controller = MethodController()

    try:
        print("Enter a command query")
        command_query = input()
        if not command_query:
            return

        command = parse(command_query)
        res = method_controller.execute(command)
        if not res:
            print("Can't recognise command")
            return

        print(res)
    except ValueError as e:
        msg = "Error: {0}".format(e)
        print(msg)

if __name__ == "__main__":
    main()
