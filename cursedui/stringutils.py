import re

_ansi_escape_regex = re.compile(
    r'\x1b('
    r'(\[\??\d+[hl])|'
    r'([=<>a-kzNM78])|'
    r'([\(\)][a-b0-2])|'
    r'(\[\d{0,2}[ma-dgkjqi])|'
    r'(\[\d+;\d+[hfy]?)|'
    r'(\[;?[hf])|'
    r'(#[3-68])|'
    r'([01356]n)|'
    r'(O[mlnp-z]?)|'
    r'(/Z)|'
    r'(\d+)|'
    r'(\[\?\d;\d0c)|'
    r'(\d;\dR))',
    re.IGNORECASE
)


def escape_ansi(line):
    return _ansi_escape_regex.sub('', line)
