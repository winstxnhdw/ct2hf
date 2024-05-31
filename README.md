# ct2hf

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![main.yml](https://github.com/winstxnhdw/ct2hf/actions/workflows/main.yml/badge.svg)](https://github.com/winstxnhdw/ct2hf/actions/workflows/main.yml)
[![formatter.yml](https://github.com/winstxnhdw/ct2hf/actions/workflows/formatter.yml/badge.svg)](https://github.com/winstxnhdw/ct2hf/actions/workflows/formatter.yml)
[![dependabot.yml](https://github.com/winstxnhdw/ct2hf/actions/workflows/dependabot.yml/badge.svg)](https://github.com/winstxnhdw/ct2hf/actions/workflows/dependabot.yml)

`ct2hf` is a friendly CLI tool for converting a supported Hugging Face transformer model to its [CTranslate2](https://github.com/OpenNMT/CTranslate2)-compatible format and uploading them to your Hugging Face repository. If you're tired of manually converting models and running into low-memory, storage, and permission issues, `ct2hf` is the perfect tool for you.

## Installation

You can install `ct2hf` via pip with the following.

```bash
pip install git+https://github.com/winstxnhdw/ct2hf
```

You can also uninstall `ct2hf` via pip with the following.

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
ct2hf openchat/openchat-3.6-8b-20240522 --files-to-copy tokenizer.model
```
