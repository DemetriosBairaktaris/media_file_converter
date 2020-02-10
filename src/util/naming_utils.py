from uuid import uuid4


def get_temp_file_name(extension):
    if '.' in extension:
        extension = extension.replace('.', '')
    return str(uuid4()) + '.' + extension

