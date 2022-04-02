import joblib
import subprocess


class dotdict(dict):
    def __getattr__(self, name):
        return self[name]


# ----------------------------------------------------------------------
def serialize(obj, path):
    """
    Pickle a Python object with joblib
    """
    with open(path, "wb") as pfile:
        joblib.dump(obj, pfile)


# ----------------------------------------------------------------------
def deserialize(path):
    """
    Extracts a joblib Python object and returns it
    """
    with open(path, "rb") as pfile:
        obj = joblib.load(pfile)
    return obj


# ----------------------------------------------------------------------
def execute_command_sync(command, show_output=True):
    print("execute command: ", command)

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

    if show_output:
        for line in iter(process.stdout.readline, ""):
            print(line)

    process.stdout.close()
    process.wait()
    return process.returncode
