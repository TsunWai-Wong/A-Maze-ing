from typing import List


class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None

    def _read_lines(file) -> None:
        """
        Read the file line by line (ignore when the line starts with #)
        Check whether the file contains lines with invalid syntax
        Save the key-value pairs in a dictionary
        """
        pass

    def _check_fields_available() -> List[str]:
        """
        Check whether the dictionary contains all mandatory keys
        Then check whether the dictionary contains all mandatory values
        The check whether all keys have values in correct datatype
        (e.g. int for all x, y values)
        """
        pass

        # WIDTH or HEIGHT is not int
        # after split by comma, x or y of ENTRY and EXIT is not int

    def _check_valid_dimension() -> bool:
        """
        check whether the file contain impossible maze parameters
        """
        # X and Y do not exceed the smallest area

        # ENTRY or EXIT is outside of the maze
        pass

    def _check_valid_names() -> bool:
        """
        helper function to check whether the output file name is valid
        """
        # output file name is not valid

        # PERFECT is not true or false (case insensitive)
        pass

    def parse_config(filename: str) -> None:
        """
        Read the file by using the helper functions in this file
        """
        try:
            with open(filename) as file:
                pass
        except ValueError as e:
            print(e)
            exit()
        except FileNotFoundError:
            print("")
            exit()
        except PermissionError:
            print("")
            exit()
