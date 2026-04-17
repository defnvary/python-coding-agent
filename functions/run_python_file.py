import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    abs_work_dir = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

    if not os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir:
        return f"Cannot execute \"{file_path}\" as it is outside the permitted working directory"

    if not os.path.isfile(target_file):
        return f"Error: \"{file_path}\" does not exists or is not a regular file"

    if target_file[len(target_file) - 2:] != "py":
        return f"Error: \"{file_path}\" is not a Python file."

    command = ["python", target_file]

    if args is not None:
        for arg in args:
            command.append(arg)

    try:
        completed_process = subprocess.run(command, cwd=abs_work_dir, capture_output=True, text=True, timeout=30)
        #print(completed_process)
        std_out = completed_process.stdout
        std_err = completed_process.stderr
        return_code = completed_process.returncode
    
        if return_code != 0:
            return f"Process ended with code {return_code}"
        
        if std_out == '' and std_err == '':
            return "No output produced"

        if std_err != '':
            return f"STDERR: \n{std_err}"

        return f"STDOUT:\n{std_out}"

    except Exception as e:
        return f"Error: {e}"