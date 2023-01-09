# living_manual

LIVING MANUAL (LIMA) is a "dirty word" search utility written in Python3.

## Description

### Base Features

LIMA will search for dirty words.  The expected format of the dirty word file is a newline-delimited list of strings.  LIMA has two Use Cases: 1. search a file for dirty words, 2. search a directory for files with dirty words.

### Encoding Support

LIMA also has limited support for alternate encoding with the `--encoding` command line argument.  Default encoding is `utf-8`.  Decode warnings are currently surpressed.

### Search Strategies

Four search strategies are currently employed.  In order of execution:

1. Treat input as a newline-delimited text file
2. Decode the entire file
3. Search the file's byte contents for encoded dirty words
4. Remove null bytes from the file's contents and search for encoded dirty words

LIMA will stop searching when a strategy has succeeded in finding at least one dirty word.

## Distribution

```
python setup.py bdist_wheel --dist-dir='dist'  # Build the wheel
ls -l dist/lima*.whl                           # Verify it was created
```

## Usage

### Installation

`pip install lima-1.1.0-py3-none-any.whl`

### Use Case 1 (file)

`lima file --help`

### Use Case 2 (directory)

`lima dir --help`


### Examples

See:

[example/LIMA_Use_Case_1.png](https://github.com/hark130/living_manual/blob/main/example/LIMA_Use_Case_1.png)

[example/LIMA_Use_Case_2.png](https://github.com/hark130/living_manual/blob/main/example/LIMA_Use_Case_2.png)
