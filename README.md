# Flask Website

Flask Website (or just "website") is a basic Flask website application that allows users to sign up, log in, and take
notes and is based on Tech With Tim's [Flask Web App Tutorial](https://github.com/techwithtim/Flask-Web-App-Tutorial).
However, the code in this repository is heavily modified from the original as it utilizes a more production-focused
approach via directory modularization, newer libraries (e.g., Bootstrap 5.2), emphasis on security, etc.

## Installation

First, `git clone` this repository, and navigate to the `flask-website` directory.

```bash
$ git clone https://github.com/JayBhatt2021/flask-website.git
$ cd flask-website
```

If you use **MacOS/Linux**, use the following commands to create your virtual environment folder and activate it,
respectively:

```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
```

Otherwise, input these commands on the **Windows** Command Prompt:

```bash
$ py -3 -m venv .venv
$ .venv\Scripts\activate
```

Now, install Flask Website and its dependencies.

```bash
$ pip install -e .
```

## Usage

Use Waitress to run the application.

```bash
$ waitress-serve --host 127.0.0.1 --port 6650 --call website:create_app
```

Open http://127.0.0.1:5000/login in the browser.
