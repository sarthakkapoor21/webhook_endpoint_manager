from collections import namedtuple

CHAR_FIELD_LENGTHS = namedtuple('CHAR_FIELD_LENGTHS', ['SHORT', 'MEDIUM', 'LONG'])(
    SHORT=127,
    MEDIUM=511,
    LONG=2047,
)
