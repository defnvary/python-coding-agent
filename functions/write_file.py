import os

def write_file(work_dir, file_path, content):
    abs_work_dir = os.path.abspath(work_dir)

    target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

    if not os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir:
        return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"

    if os.path.isdir(target_file):
        return f"Error: Cannot write to {file_path} as it is a directory"

    # make sure all parent directories of the file_path exists
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    try:
        with open(target_file, "w") as file:
            file.write(content)

        return f"Succesfully wrote to '{file_path}'. {len(content)} characters written."

    except Exception as e:
        return f"Error: {e}"