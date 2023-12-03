import textwrap
from html.parser import HTMLParser

from ._helpers import logger


__all__ = [
    "parse_prompt_html_to_md",
]


def parse_prompt_html_to_md(html: str) -> str:
    parser = PromptHTMLParser()
    parser.feed(html)
    return parser.get_result()


class PromptHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._tagstack: list[Element] = []
        self._processing = False
        self._comment = False
        self._articles = []
        self._read_title = False
        self._title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrdict = dict(attrs)

        if tag == "title":
            self._read_title = True

        if tag == "article" and attrdict.get("class") == "day-desc":
            logger.debug("Found starting article tag")
            self._processing = True
            self._tagstack.append(Article(attrdict))
            return

        elif not self._processing:
            return

        logger.debug(f"processing tag: {tag} --  [{_list_tags(self)}]")
        ElementType = get_element_type(tag)
        if not ElementType:
            logger.debug(f"Ignoring: {tag}")
            return

        if self._tagstack and type(self._tagstack[-1]) is ElementType:
            logger.debug("detected a possibly erroneous tag, treating it as an ending tag instead")
            return self.handle_endtag(tag)

        self._tagstack.append(ElementType(attrdict))

    def handle_endtag(self, tag) -> None:
        if not self._processing:
            return

        logger.debug(f"closing tag: {tag} -- [{_list_tags(self)}]")
        if self._tagstack[-1].name != tag:
            logger.debug(f"Ignoring ending tag: {tag}")
            return

        if tag == "article":
            article = self._tagstack.pop()
            assert not self._tagstack
            self._articles.append(article.format())
            self._processing = False
            return

        element = self._tagstack.pop()
        self._tagstack[-1].add_element(element)

    def handle_data(self, data: str) -> None:
        if self._comment:
            self._comment = False
            return

        elif self._read_title:
            self._title = data
            self._read_title = False
            return

        elif not self._processing:
            return

        self._tagstack[-1].add_data(data)

    def handle_comment(self, _):
        self._comment = True

    def get_result(self) -> str:
        result = f"# {self._title}\n\n{"\n\n".join(self._articles)}"
        result = result.replace("  ", " ")
        result.rstrip("\n")
        result += "\n"
        return result


type Attrs = dict[str, str | None]
type Element = A | Article | Code | Em | H2 | LI | P | Span | UL
_factory: dict[str, type[Element]] = {}


def register_element_type[ET: type[Element]](et: ET) -> ET:
    assert (
        et.name not in _factory
    ), f"{et.name} already registered by {_factory[et.name]}"
    _factory[et.name] = et  # type: ignore | shhh... it will be okay
    return et


def get_element_type(name: str) -> type[Element] | None:
    return _factory.get(name, None)


@register_element_type
class A:
    name = "a"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: str = ""
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        self._data = data

    def add_element(self, element: Element) -> None:
        self._data += element.format()

    def format(self) -> str:
        return f"[{self._data}]({self._attrs.get("href", "")})"


@register_element_type
class Article:
    name = "article"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: list[str] = []
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        if data.strip():
            raise UnsupportedSubElement(type(self), data)

    def add_element(self, element: Element) -> None:
        self._data.append(element.format())

    def format(self) -> str:
        return "\n\n".join(self._data)


@register_element_type
class Code:
    name = "code"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: list[str] = []
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        self._data.append(data)

    def add_element(self, element: Element) -> None:
        self._data.append(element.format())

    def format(self) -> str:
        str_data = "".join(self._data).strip()
        if "\n" in str_data:
            return f"```\n{str_data}\n```"
        else:
            return f"`{str_data}`"


@register_element_type
class Em:
    name = "em"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: list[str] = []
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        self._data.append(data)

    def add_element(self, element: Element) -> None:
        self._data.append(element.format())

    def format(self) -> str:
        if self._attrs:
            return f"**{"".join(self._data)}**"
        else:
            return f"*{"".join(self._data)}*"


@register_element_type
class H2:
    name = "h2"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: list[str] = []
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        self._data.append(data)

    def add_element(self, element: Element) -> None:
        self._data.append(element.format())

    def format(self) -> str:
        return f"## {"".join(self._data)}"


@register_element_type
class LI:
    name = "li"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: list[str] = []
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        self._data.append(data)

    def add_element(self, element: Element) -> None:
        self._data.append(element.format())

    def format(self) -> str:
        lines = textwrap.wrap(
            "".join(self._data),
            width=80,
            initial_indent="- ",
            subsequent_indent=" " * 4,
        )
        return "\n".join(lines)


@register_element_type
class P:
    name = "p"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: list[str] = []
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        self._data.append(data)

    def add_element(self, element: Element) -> None:
        self._data.append(element.format())

    def format(self) -> str:
        return "\n".join(textwrap.wrap("".join(self._data), width=80))


@register_element_type
class Span:
    name = "span"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: str = ""
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        self._data = data

    def add_element(self, element: Element) -> None:
        self._data += element.format()

    def format(self) -> str:
        return self._data


@register_element_type
class UL:
    name = "ul"

    def __init__(self, attrs: Attrs | None = None) -> None:
        self._data: list[str] = []
        self._attrs = attrs or {}

    def add_data(self, data: str) -> None:
        if data.strip():
            raise UnsupportedSubElement(type(self), data)

    def add_element(self, element: Element) -> None:
        if isinstance(element, LI):
            self._data.append(element.format())
        else:
            raise UnsupportedSubElement(root=type(self), data=element)

    def format(self) -> str:
        return "\n".join(self._data)


class UnsupportedSubElement(RuntimeError):
    def __init__(self, root: type[Element], data: str | Element) -> None:
        str_data = data if isinstance(data, str) else data.format()
        super().__init__(
            f"Element of type {type(data).__name__!r} is unsupported by parent"
            f" of type {root.__name__!r}: {str_data}"
        )


def _list_tags(x: PromptHTMLParser) -> str:
    return ', '.join(tag.name for tag in x._tagstack)
