import sys
import random
from config_parser import Config, ParseError
from maze import Maze, HuntAndKillGenerator, add_42_pattern
from path_finder import PathFinder
from output_writer import OutputWriter
from gui.renderer import Renderer


def check_argv() -> None:
    """
    Validate command line arguments.
    Ensures exactly one configuration file argument is provided.
    """
    if len(sys.argv) < 2:
        raise ParseError("config file is not provided as an argument")
    if len(sys.argv) > 2:
        raise ParseError("extra argument is provided")


def check_visualiable(config: Config) -> None:
    """
    Ensures that the width and height do not exceed the maximum
    allowed size for visualization.

    Args:
    config (Config): Configuration containing dimensions.
    """
    if config.width > 429:
        raise Exception("Maximum width to be visualised is "
                        "429 cells. See output file for the result.")
    elif config.height > 429:
        raise Exception("Maximum height to be visualised is "
                        "429 cells. See output file for the result.")


def main() -> None:
    """
    Program entry point for maze generation and execution.

    Parses configuration, generates a maze, finds a path,
    writes output, and renders in a Graphical User Interface.
    """
    try:
        check_argv()
        config = Config()
        config.parse_config(sys.argv[1])

        maze = Maze(config.width, config.height)
        add_42_pattern(maze)
        config.seed = config.seed or random.randint(1, 10000)
        generator = HuntAndKillGenerator(config.seed)
        generator.generate(maze)

        pathfinder = PathFinder(maze)
        entry_cell = maze.get_cell(*config.entry)
        exit_cell = maze.get_cell(*config.exit)
        path = pathfinder.find_path(entry_cell, exit_cell)

        writer = OutputWriter(config, maze, path[1])
        writer.write_output()

        check_visualiable(config)
        renderer = Renderer(config, maze, path)
        renderer.run()

    except ParseError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
