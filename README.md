# Temp Files Manager

Lightweight manager for creating, tracking, and cleaning temporary directories used by other modules (e.g., GitHub operations). It centralizes temp path selection via project configuration and provides a tiny, safe API.

## Overview
- Centralizes where temporary working folders are created across the project
- Resolves a base temp directory from `.config` under `temp_files_manager.path`
- Creates uniquely named subdirectories for each operation and cleans them up safely

## Features
- Base dir resolution from config (Windows and Unix):
	- `.config.temp_files_manager.path.unix_temp` on Linux/macOS
	- `.config.temp_files_manager.path.windows_temp` on Windows
- Create and track per-operation temp directories
- Recursive cleanup of a specific path or all tracked paths
- Small, dependency-light implementation

## Configuration
This module reads its base temp directory from the consolidated `.config` file. The expected keys are under `temp_files_manager.path`:

```json
{
	"module_name": "temp_files_manager",
	"path": {
		"data": "./project/data/temp_files_manager",
		"unix_temp": "/tmp/github_api_core",
		"windows_temp": "C:\\Temp\\github_api_core"
	}
}
```
Make sure `.config` includes the `unix_temp` (or `windows_temp`) path you prefer for temporary work.

## Usage

Basic creation and cleanup:

```python
from managers.temp_files_manager.temp_files_manager import TempFilesManager

tfm = TempFilesManager()  # base dir resolved from .config
work_dir = tfm.make_dir(prefix="clone")

# ... do work that writes into work_dir ...

tfm.cleanup(work_dir)  # remove this temp directory
```

Clean up everything tracked so far:

```python
tfm.cleanup_all()
```

Override the base directory explicitly (bypasses config resolution):

```python
tfm = TempFilesManager(base_dir="/tmp/my_module")
```

## API

```python
class TempFilesManager:
		def __init__(self, base_dir: str | None = None) -> None: ...
		def make_dir(self, prefix: str = "tmp") -> str: ...
		def cleanup(self, path: str) -> None: ...
		def cleanup_all(self) -> None: ...
```

Notes:
- `make_dir` returns the absolute path to a newly created directory under the resolved base dir.
- `cleanup` removes a path recursively. It’s safe to call even if the path no longer exists.
- `cleanup_all` removes all paths created via this instance’s `make_dir` during its lifetime.

## Module Structure

```
managers/temp_files_manager/
├─ __init__.py                 # package marker
├─ .config_template            # default config schema for this module
├─ README.md                   # this file
├─ temp_files_manager.py       # implementation
└─ init.yaml                   # module metadata
```

## Troubleshooting
- The `.config` file doesn’t contain `temp_files_manager.path.*` keys:
	- Add the keys to `.config` or pass a `base_dir` explicitly to the constructor.
- Permission errors when creating or deleting temp directories:
	- Ensure the configured base directory is writable by your user.
- On Windows, ensure the configured `windows_temp` path exists or is creatable.

## Design notes
- Uses `shutil.rmtree(..., ignore_errors=True)` for resilient cleanup.
- Tracks created paths in-memory per instance; long-lived processes can call `cleanup_all` to ensure no leftovers.
- Minimal logging via the project’s centralized logger.