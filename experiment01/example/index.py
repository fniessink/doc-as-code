import datetime

Context = dict[str, str | list[str]] | None  # FIXME: duplicated from ..main.py


def process(context: Context) -> None:
    """Add a timestamp to the context."""
    context["now"] = datetime.datetime.now().replace(microsecond=0)
    if "status" in context:
        context["status"] = f"Status: {context['status']}"
