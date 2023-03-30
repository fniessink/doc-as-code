import importlib
import json
import string
import sys
from pathlib import Path


Context = dict[str, str | list[str]] | None


def process_json(path: Path, context: Context) -> None:
    """Read the JSON file, merge the context with the JSON file, and process its contents."""
    context = context or {}
    with path.open("r") as json_file:
        json_contents = json.load(json_file)
    paths = [path.parent / Path(filename) for filename in json_contents.get("contents")]
    process_files(paths, context | json_contents)


def process_md(path: Path, context: Context) -> None:
    """Read the Markdown file, substite the context, and print the resulting Markdown to stdout."""
    with path.open("r") as markdown_file:
        print(string.Template(markdown_file.read()).substitute(context or {}))


def process_py(path: Path, context: Context) -> Context:
    """Import the Python file and let it manipulate the context.

    Assumes the Python file contains a method: `process(context: Context) -> Context`.
    """
    module = importlib.import_module(".".join(path.with_suffix("").parts))
    return module.process(context)


def process_files(paths: list[Path], context: Context = None) -> None:
    """Process the files using the appropriate processors, determined by the file extensions."""
    for path in paths:
        process = globals()[f"process_{path.suffix.strip('.')}"]  # Look up the process function by path extension
        process(path, context)


if __name__ == "__main__":
    process_files([Path(filename) for filename in sys.argv[1:]])