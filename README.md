# Step-1: Download repository

- Clone/download the repository,

    `git clone git@github.com:dhsh-checkmk/debug-playwright-focus.git`

    or [download](https://github.com/dhsh-checkmk/debug-playwright-focus/archive/refs/heads/main.zip) it as a zip file.

- Navigate to the root directory of the repository.

# Step-2: Checkmk website and password

- Download, load and run Checkmk within a docker container.
  
    Use [install script](./install-checkmk-docker.sh) to perform the actions.
  
    **NOTE**: ports `8080` and `8000` need to be availble before `install script` execution.
    Check the `install script` for docker container initialization.

    In-depth installation details can be found [here](https://docs.checkmk.com/latest/en/introduction_docker.html).

- Update password within [test_debug.py](./test_debug.py).
    
    If successful, the `install script` outputs the (admin) user and password.
    Copy this password and pastes it's value within `test_debug::PASSWORD (line 16)`.

- Validate that checkmk website can accessed at `http://127.0.0.1:8080/cmk/check_mk/`


# Step-3: Enable virtual environment

```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv)$ pip install -U pip wheel
(.venv)$ pip install -r requirements.txt
```

# Step-4: Run the test

```
(.venv)$ pytest test_debug.py
```