# ct2hf

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-blue)](https://www.python.org/)
[![main.yml](https://github.com/winstxnhdw/ct2hf/actions/workflows/main.yml/badge.svg)](https://github.com/winstxnhdw/ct2hf/actions/workflows/main.yml)
[![formatter.yml](https://github.com/winstxnhdw/ct2hf/actions/workflows/formatter.yml/badge.svg)](https://github.com/winstxnhdw/ct2hf/actions/workflows/formatter.yml)

`ct2hf` is a user-friendly CLI tool designed to simplify the process of converting supported Hugging Face transformer models into a [CTranslate2](https://github.com/OpenNMT/CTranslate2)-compatible format. Additionally, it seamlessly uploads the converted model to your Hugging Face repository. No interaction required!

## Features

- **Bloat-Free**: Automatically cleans up all dependencies, even if the program has terminated unexpectedly
- **Zero Interaction**: Convert, quantise and upload your models to Hugging Face all while brewing your coffee
- **Memory Efficient**: Utilises the least amount of memory possible to handle large model conversions
- **Intelligent Defaults**: Avoids common permission and storage pitfalls with sensible defaults
- **Anti-LFS**: Only uses Git LFS when necessary, avoiding unnecessary issues that arise from using LFS

## Usage

> [!NOTE]\
> You have to be logged in to Hugging Face to upload the converted model onto your account. You can do this by running `uvx --no-cache --from huggingface-hub huggingface-cli login`.

You may use `pip` to install `ct2hf` but we recommended using [uv](https://github.com/astral-sh/uv) to avoid polluting your Python environment.

```bash
uvx --no-cache --python 3.13 --from git+https://github.com/winstxnhdw/ct2hf ct2hf --help
```

By default, `ct2hf` avoids leaving behind any unnecessary files. If you would like to preserve the downloaded models, you can use the `--preserve-models` flag. Additionally, if `--quantisation` is not specified, the quantisation type defaults to `int8`.

> [!TIP]\
> `ct2hf` has some memory usage optimisations that may not be compatible with some models. If you encounter any issues, try using the `--compatibility` flag.

```yaml
usage: ct2hf

convert and upload a transformer model to huggingface

positional arguments:
  model-id              transformer model to convert

options:
  --output-name         name of the output model
  --files-to-copy       files to copy to the output model
  --preserve-models     do not delete the downloaded models
  --revision            revision of the model to convert
  --quantisation        none, int8_float32, int8_float16, int8_bfloat16, int16, float16, bfloat16, float32
  --compatibility       use compatibility mode at the cost of higher memory usage
```

### Example

The minimal usage of `ct2hf` involves specifying the model ID of the transformer model you would like to convert.

```bash
ct2hf openchat/openchat-3.6-8b-20240522
```

You can also specify the name of the output model.

```bash
ct2hf openchat/openchat-3.6-8b-20240522 --output-name openchat-3.6-ct2-int8
```

You can also specify the files to copy to the output model.

```bash
ct2hf openchat/openchat-3.6-8b-20240522 --files-to-copy tokenizer.json
```
