from beanie import Document, Indexed


class Game(Document):
    name: Indexed(str, unique=True)  # type: ignore
    rules_url: str
    enabled: bool
    description: str
    display_name: str
