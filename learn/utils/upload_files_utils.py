# Imports Python
import os
import tempfile
import magic


# Import Utils
from learn.utils.supabase_utils import supabase_connect


def upload_file_to_supabase(file, file_name, buckets):
    supabase = supabase_connect()

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            for chunk in file.chunks():
                tmp_file.write(chunk)

        mime_type = magic.Magic()
        content_type = mime_type.from_file(tmp_file.name)

        with open(tmp_file.name, "rb") as tmp_file:
            upload = supabase.storage.from_(buckets).upload(
                file_name, tmp_file, {"content-type": content_type}
            )

        os.remove(tmp_file.name)

        url_file = supabase.storage.from_(buckets).get_public_url(file_name)
        return url_file
    except Exception as e:
        raise e
