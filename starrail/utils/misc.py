import functools
import hashlib
import importlib
import io

import qrcode


@functools.lru_cache
def lazy_import(name, package=None):
    return importlib.import_module(name, package)


@functools.lru_cache
def sha1(data):
    hasher = hashlib.sha1()
    if isinstance(data, str):
        data = data.encode('utf-8')
    hasher.update(data)
    return hasher.hexdigest()


def create_qrcode_image(
    data,
    version=1,
    error_correction=qrcode.ERROR_CORRECT_L,
    box_size=10,
    border=1,
    fill_color='black',
    back_color='white',
) -> bytes:
    code = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    code.add_data(data=data)
    code.make(fit=True)
    stream = io.BytesIO()
    image = code.make_image(fill_color=fill_color, back_color=back_color)
    image.save(stream, format='PNG')

    return stream.getvalue()
