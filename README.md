# A minimal LLM powered coding agent

This agent takes the natural language input ("example - explain how does the calculator render results to the console?") and attempts to read, generate, edit and execute the code. I uses Gemini API for generation (function calling) and python subprocess module for execution.

## Config

In `config.py` you can set

- `MODEL_NAME` - Name of the Gemini model
- `BUFFER_SIZE_MAX` - Maximum input size, currently set to 10,000 characters
- `WORKING_DIR` - The model will have access to this directory and its subdirectories
- `MAX_ITER` - Maximum number of iterations that we want model to loop through

Create a `.env` in root directory of this project and set `GEMINI_API_KEY` there.

## Instructions

This project uses `uv` for package and environment management. You can install uv from [here](https://github.com/astral-sh/uv).

In root directory, run

```bash
uv venv && uv sync
```

Then,
```bash
uv run main.py "you query"
```

You can use optional `--verbose` argument to see the functions called and additional info like token count.

*Note* : There is a demo `calculator` project inside `calculator` directory for you to experiment with.

This project was built using instructions from [boot.dev](https://boot.dev). The calculator source is taken from their course.