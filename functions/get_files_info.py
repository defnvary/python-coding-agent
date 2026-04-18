import os
from google.genai import types


def get_files_info(work_dir, dir="."):
    try:
        abs_work_dir = os.path.abspath(work_dir)
        target_dir = os.path.normpath(os.path.join(abs_work_dir, dir))

        if os.path.commonpath([abs_work_dir, target_dir]) != abs_work_dir:
            return f"Error: Cannot list {dir} as it is outside the permitted work directory"

        if not os.path.isdir(target_dir):
            return f"Error: '{dir}' is not a directory"

        files_info = []

        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)

            files_info.append(f"- {filename}: file_size={file_size}, is_dir={is_dir}")

        return "\n".join(files_info)

    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "dir": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            )
        },
    ),
)
