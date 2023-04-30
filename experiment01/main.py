import argparse
import importlib
import json
import string
from collections import defaultdict
from pathlib import Path
from typing import NoReturn


Context = dict[str, str | list[str]] | None


def process_json(path: Path, context: Context) -> None:
    """Read the JSON file, merge the context with the JSON file, and process its contents."""
    context = context or {}
    with path.open("r") as json_file:
        json_contents = json.load(json_file)
    paths = [path.parent / Path(filename) for filename in json_contents.get("_paths")]
    process_files(paths, context | json_contents)


def process_md(path: Path, context: Context) -> None:
    """Read the Markdown file, substitute the context, and print the resulting Markdown to stdout."""
    mapping = defaultdict(str, **context)  # Insert empty strings for missing substitutions
    with path.open("r") as markdown_file:
        print(string.Template(markdown_file.read()).substitute(mapping))


def process_py(path: Path, context: Context) -> None:
    """Import the Python file and let it manipulate the context.

    Assumes the Python file contains a method: `process(context: Context) -> None`.
    """
    module = importlib.import_module(".".join(path.with_suffix("").parts))
    module.process(context)


def process_files(paths: list[Path], context: Context = None) -> None:
    """Process the files using the appropriate processors, determined by the file extensions."""
    for path in paths:
        process = globals()[f"process_{path.suffix.strip('.')}"]  # Look up the process function by path extension
        process(path, context)


def parse_args() -> tuple[Path, Context] | NoReturn:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="JSON file to process")
    namespace, unknown = parser.parse_known_args()
    path = Path(namespace.filename)
    context = dict([argument.strip("-").split("=") for argument in unknown])  # Convert ["--foo=bar"] into dict(foo=bar)
    return path, context


if __name__ == "__main__":
    filename, context = parse_args()
    process_files([filename], context)
