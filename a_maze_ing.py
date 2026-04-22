import sys
from config_parser import Config, ParseError
from maze import Maze, HuntAndKillGenerator, add_42_pattern
from path_finder import PathFinder
from output_writer import OutputWriter
from gui.renderer import Renderer


def check_argv() -> None:
    if len(sys.argv) < 2:
        raise ParseError("config file is not provided as an argument")
    if len(sys.argv) > 2:
        raise ParseError("extra argument is provided")


def main() -> None:
    try:
        check_argv()
        config = Config()
        config.parse_config(sys.argv[1])

        maze = Maze(config.width, config.height)
        add_42_pattern(maze)
        config.seed = config.seed or 42
        generator = HuntAndKillGenerator(config.seed)
        generator.generate(maze)

        pathfinder = PathFinder(maze)
        entry_cell = maze.get_cell(*config.entry)
        exit_cell = maze.get_cell(*config.exit)
        path = pathfinder.find_path(entry_cell, exit_cell)

        writer = OutputWriter(config, maze, path[1])
        writer.write_output()

        renderer = Renderer(config, maze, path)
        renderer.render()

    except ParseError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
