from typing import Dict


class ParseError(Exception):
    pass


class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None

    def _parse_tuple(self, fieldname: str, value: str | None) -> tuple[int, int] | None:
        if value is None:
            raise ParseError(f"Missing mandatory key: {fieldname}")
        parts = value.split(",")
        if len(parts) != 2:
            raise ParseError(f"Invalid tuple format: {value}")
        if not parts[0].strip() or not parts[1].strip():
            raise ParseError(f"Invalid tuple format: {value}")
        try:
            x, y = parts[0].strip(), parts[1].strip()
            return int(x), int(y)
        except ValueError:
            raise ParseError(f"Invalid tuple format: {value}")

    def _parse_bool(self, fieldname: str, value: str) -> bool:
        if value is None:
            raise ParseError(f"Missing mandatory key: {fieldname}")
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        raise ParseError(f"Invalid boolean: {value}")

    def _read_lines(self, file) -> Dict[str, str]:
        """
        Read the file line by line (ignore when the line starts with #)
        Check whether the file contains lines with invalid syntax
        Save the key-value pairs in a dictionary
        """
        data = {}
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            else:
                line_items = line.split("=")
                if len(line_items) != 2:
                    raise ParseError("At least 1 line has invalid syntax")
                key, value = line_items[0].strip(), line_items[1].strip()
                if not key:
                    raise ParseError("A key must be provided on each line")
                if not value:
                    raise ParseError("A value must be provided on each line")
                data[key.upper()] = value
        return data

    def _check_fields_available(self, data: Dict[str, str]) -> None:
        """
        Check whether the dictionary contains all mandatory keys
        Then check whether the dictionary contains all mandatory values
        The check whether all keys have values in correct datatype
        (e.g. int for all x, y values)
        """
        try:
            self.width = int(data["WIDTH"])
            self.height = int(data["HEIGHT"])
            self.entry = self._parse_tuple("ENTRY", data.get("ENTRY"))
            self.exit = self._parse_tuple("EXIT", data.get("EXIT"))
            if "OUTPUT_FILE" not in data:
                raise ParseError("Missing mandatory key: OUTPUT_FILE")
            self.output_file = data["OUTPUT_FILE"].strip()
            if not self.output_file:
                raise ParseError("Invalid value: OUTPUT_FILE cannot be empty")
            self.perfect = self._parse_bool("PERFECT", data.get("PERFECT"))
            self.seed = int(data["SEED"]) if "SEED" in data else None
        except KeyError as e:
            raise ParseError(f"Missing mandatory key: {e}")
        except ValueError as e:
            raise ParseError(f"Invalid value: {e}")

    def _check_valid_dimension(self) -> bool:
        """
        check whether the file contain impossible maze parameters
        """
        # X and Y do not exceed the smallest area
        if self.width < 9:
            raise ParseError("Width value is too small")
        if self.height < 7:
            raise ParseError("Height value is too small")
        # Entry and exit must be different
        if self.entry == self.exit:
            raise ParseError("Entry and exit must be different")
        # ENTRY or EXIT is outside of the maze
        if (self.entry[0] >= self.width or self.entry[0] < 0 or
           self.entry[1] >= self.height or self.entry[1] < 0):
            raise ParseError("ENTRY position is outside of the maze")
        if (self.exit[0] >= self.width or self.exit[0] < 0 or
           self.exit[1] >= self.height or self.exit[1] < 0):
            raise ParseError("EXIT position is outside of the maze")
        # ENTRY or EXIT lies on the protected area
        if False:
            raise ParseError("ENTRY or EXIT cannot be in the protected area")

    def parse_config(self, filename: str) -> None:
        """
        Read the file by using the helper functions in this file
        """
        try:
            with open(filename) as file:
                data = self._read_lines(file)
            self._check_fields_available(data)
            self._check_valid_dimension()

        except FileNotFoundError:
            raise ParseError("Config file is not found")
        except PermissionError:
            raise ParseError("Config file cannot be opened due to permission error")
