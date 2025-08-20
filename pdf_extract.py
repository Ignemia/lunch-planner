import typing
import enum

def extract_pdf_data(data_stream: str, extract_type: enum.IntEnum) -> typing.Optional[typing.Dict]:
    assert extract_type.value != 0
    assert len(data_stream) > 0
