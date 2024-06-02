# ct2hf

[![python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://www.python.org/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![main.yml](https://github.com/winstxnhdw/ct2hf/actions/workflows/main.yml/badge.svg)](https://github.com/winstxnhdw/ct2hf/actions/workflows/main.yml)
[![formatter.yml](https://github.com/winstxnhdw/ct2hf/actions/workflows/formatter.yml/badge.svg)](https://github.com/winstxnhdw/ct2hf/actions/workflows/formatter.yml)
[![dependabot.yml](https://github.com/winstxnhdw/ct2hf/actions/workflows/dependabot.yml/badge.svg)](https://github.com/winstxnhdw/ct2hf/actions/workflows/dependabot.yml)

`ct2hf` is a user-friendly CLI tool designed to simplify the process of converting supported Hugging Face transformer models into a [CTranslate2](https://github.com/OpenNMT/CTranslate2)-compatible format. Additionally, it uploads the converted model to your Hugging Face repository. With `ct2hf`, you can avoid the hassle of manual conversions and the common issues of low memory, storage limitations, and permission errors.

## Installation

You can install `ct2hf` via `pip` with the following.

```bash
pip install git+https://github.com/winstxnhdw/ct2hf
```

Then, you can uninstall `ct2hf` and all of its dependencies with the following.

```bash
pip uninstall ct2hf
```

## Usage

By default, `ct2hf` avoids leaving behind any unnecessary files. If you would like to preserve the downloaded models, you can use the `--preserve-models` flag.

```yaml
usage: ct2hf

convert and upload a transformer model to huggingface

positional arguments:
  model-id              transformer model to convert

options:
  --output-name         name of the output model
  --files-to-copy       files to copy to the output model
  --preserve-models     do not delete the downloaded models
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
ct2hf openchat/openchat-3.6-8b-20240522 --files-to-copy tokenizer.json tokenizer_config.json
```
