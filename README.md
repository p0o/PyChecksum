# PyChecksum

A simple CLI tool to create unified checksum from all the files and directories within a certain path. You can use it within your CI/CD pipeline and automations to detect change or deterministically address a specific artifact.

# How to use?

To view help:

```bash
./pychecksum -h
```

Get the checksum of current directories files and sub-directories:

```bash
./pychecksum
```

Create a checksum of all the files and sub-directoreis within `src` directory:

```bash
./pychecksum -d ./src
```

Exclude `node_modules` and `__pycache__` directories:

```bash
./pychecksum -d . -e node_modules -e __pycache__
```

Limit the size of the checksum to 10 characters:

```bash
./pychecksum -s 10
```
