import os
from config import BUFFER_SIZE_MAX
from google.genai import types


def get_file_content(work_dir, file_path):
    abs_work_dir = os.path.abspath(work_dir)
    target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

    if os.path.commonpath([abs_work_dir, target_file]) != abs_work_dir:
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"

    if not os.path.isfile(target_file):
        return f"Error: File not found or is not a regular file: '{file_path}'"

    try:
        with open(target_file, "r") as file:
            content = ""
            for ch in file.read(BUFFER_SIZE_MAX):
                content += ch

            return content

    except FileNotFoundError as e:
        print(f"Error: {e}")


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read content of file in a specified path relative to the working directory, returns string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of the file, relative to working directory to read content from",
            )
        },
    ),
)
