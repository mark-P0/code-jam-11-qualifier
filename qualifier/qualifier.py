from enum import auto, StrEnum
import warnings

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


def convert_word_to_piglatin(word: str) -> str:
    vowels = "aeiou"
    if word[0].lower() in vowels:
        return word + "way"

    consonant_slice_end = 0
    for idx, letter in enumerate(word):
        if letter.lower() in vowels:
            consonant_slice_end = idx
            break

    cluster = word[0:consonant_slice_end]
    return word[consonant_slice_end:] + cluster + "ay"


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode

        str(self)  # Trigger quote conversion on creation

    def __str__(self) -> str:
        return self._create_variant()

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """

        if self.mode == VariantMode.UWU:
            return self._create_uwu_variant()
        if self.mode == VariantMode.PIGLATIN:
            return self._create_piglatin_variant()

        return self.quote

    def _create_uwu_variant(self) -> str:
        partial = (
            self.quote.replace("L", "W")
            .replace("l", "w")
            .replace("R", "W")
            .replace("r", "w")
        )
        variant = partial.replace(" U", " U-U").replace(" u", " u-u")

        if variant == self.quote:
            raise ValueError("Quote was not modified")

        if len(variant) > MAX_QUOTE_LENGTH:
            warnings.warn("Quote too long, only partially transformed")
            variant = partial

        return variant

    def _create_piglatin_variant(self) -> str:
        sep = " "
        words = self.quote.split(sep)
        variant = sep.join(
            convert_word_to_piglatin(word) for word in words
        ).capitalize()

        if len(variant) > MAX_QUOTE_LENGTH:
            raise ValueError("Quote was not modified")

        return variant


def build_quote_str_from_parts(parts: list[str], sep: str) -> str:
    quote_str = sep.join(parts).replace('"', "").replace("“", "").replace("”", "")
    if len(quote_str) > MAX_QUOTE_LENGTH:
        raise ValueError("Quote is too long")

    return quote_str


def add_quote_to_database_safely(quote: Quote):
    try:
        Database.add_quote(quote)
    except DuplicateError:
        print("Quote has already been added previously")


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """

    sep = " "
    match command.split(sep):
        # TODO Check for "trailing" arguments?
        case ["quote", "list"]:
            message = "\n".join(f"- {quote}" for quote in Database.get_quotes())
            print(message)

        # TODO For quotes, check if quote is valid? e.g only 2 quotation marks

        case ["quote", "piglatin", *quote_str_parts]:
            quote_str = build_quote_str_from_parts(quote_str_parts, sep)
            quote = Quote(quote_str, VariantMode.PIGLATIN)

            add_quote_to_database_safely(quote)

        case ["quote", "uwu", *quote_str_parts]:
            quote_str = build_quote_str_from_parts(quote_str_parts, sep)
            quote = Quote(quote_str, VariantMode.UWU)

            add_quote_to_database_safely(quote)

        case ["quote", *quote_str_parts]:
            quote_str = build_quote_str_from_parts(quote_str_parts, sep)
            quote = Quote(quote_str, VariantMode.NORMAL)

            add_quote_to_database_safely(quote)

        case _:
            raise ValueError("Invalid command")


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
