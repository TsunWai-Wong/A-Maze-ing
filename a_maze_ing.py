import sys
from config_parser import Config, ParseError


def main() -> None:
    try:
        if len(sys.argv) < 2:
            raise ParseError("Error: config file is not provided as an argument")
        if len(sys.argv) > 2:
            raise ParseError("Error: extra argument is provided")
        config = Config()
        config.parse_config(sys.argv[1])

    except ParseError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
