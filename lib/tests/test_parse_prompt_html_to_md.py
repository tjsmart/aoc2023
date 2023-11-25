from pathlib import Path

import pytest

from .._prompt_html_parser import parse_prompt_html_to_md


THIS_DIR = Path(__file__).resolve().parent


@pytest.mark.parametrize(
    ("html_file", "expected_md_file"), [
        ("./prompt_examples/prompt_one_article.html.txt", "./prompt_examples/expected_prompt_one_article.md.txt"),
        ("./prompt_examples/prompt_two_articles.html.txt", "./prompt_examples/expected_prompt_two_articles.md.txt"),
    ]
)
def test_parser_matches_saved_templates(html_file: str, expected_md_file: str):
    html = (THIS_DIR / html_file).read_text()
    expected_md = (THIS_DIR / expected_md_file).read_text()

    actual_md = parse_prompt_html_to_md(html)

    assert actual_md == expected_md
