import io

import pytest
from helpers import unhex

from unblob.handlers.archive.tar import _get_tar_end_offset

TAR_BLOCK = unhex(
    """\
00000000  74 65 73 74 2f 66 6f 6f  2e 64 61 74 00 00 00 00  |test/foo.dat....|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000060  00 00 00 00 30 30 30 30  36 34 34 00 30 30 30 31  |....0000644.0001|
00000070  37 35 30 00 30 30 30 30  31 34 34 00 30 30 30 30  |750.0000144.0000|
00000080  30 30 30 30 32 30 30 00  31 34 31 36 30 30 35 35  |0000200.14160055|
00000090  37 32 35 00 30 31 30 32  32 33 00 20 30 00 00 00  |725.010223. 0...|
000000a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000100  00 75 73 74 61 72 20 20  00 00 00 00 00 00 00 00  |.ustar  ........|
00000110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000200  c4 d8 da 39 27 3e 70 1b  ec 79 fc 36 d7 e4 4e 58  |...9'>p..y.6..NX|
00000210  e7 ef 90 0d 83 26 a9 f6  71 a2 42 b0 19 43 d3 ea  |.....&..q.B..C..|
00000220  29 48 38 39 cd a0 e9 ad  38 1e 53 3f 60 4d e1 2a  |)H89....8.S?`M.*|
00000230  de 8b ca f8 64 66 c1 0d  5e 4c aa fa cc c5 ab 73  |....df..^L.....s|
00000240  1d 2d ec f1 1b 5f aa 4a  b4 c7 94 95 00 60 3a a3  |.-..._.J.....`:.|
00000250  42 d9 45 2c d8 b1 99 11  da f7 33 34 7d 21 2f d4  |B.E,......34}!/.|
00000260  b3 f6 cd c6 62 80 d1 39  0c 47 c1 fe 30 15 42 39  |....b..9.G..0.B9|
00000270  7b fd 92 94 f7 fe 90 94  77 97 8c 76 61 e7 2c 13  |{.......w..va.,.|
00000280  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000400  # Padded to 2*512 byte blocks
"""
)

PADDED_TO_DEFAULT_BLOCKING_FACTOR = unhex(
    """\
00000400  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00002800"""
)


@pytest.mark.parametrize(
    "contents",
    (
        pytest.param(
            TAR_BLOCK + PADDED_TO_DEFAULT_BLOCKING_FACTOR,
            id="padded-to-default-blocking-factor",
        ),
        pytest.param(TAR_BLOCK, id="not-padded"),
    ),
)
def test_offset(contents: bytes):
    f = io.BytesIO(contents)

    offset = _get_tar_end_offset(f)
    assert offset == len(contents)
