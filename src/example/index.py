import datetime

Context = dict[str, str | list[str]] | None  # FIXME: duplicated from ..main.py


def process(context: Context) -> Context:
    """Add a timestamp to the context."""
    context["now"] = datetime.datetime.now().replace(microsecond=0)
    return context
