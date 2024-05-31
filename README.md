# ct2hf

`ct2hf` is a friendly CLI tool for converting a supported Hugging Face transformer model to its [CTranslate2](https://github.com/OpenNMT/CTranslate2)-compatible format and uploading them to your Hugging Face repository. If you're tired of manually converting models and running into low-memory or storage issues, `ct2hf` is the perfect tool for you.

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

```bash
ct2hf openchat/openchat-3.6-8b-20240522
```
