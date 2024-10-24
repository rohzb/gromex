# gromex (GROMmunio EXport)

`gromex` is a Python module for exporting data from Grommunio. It can be used either directly as a Python library or as a command-line utility to export calendar data.

- **Library**: Programmatically connect to a Grommunio CalDAV server and export calendar data using the `GrommunioCalendars` class.
- **Command-line Utility**: Easily export calendar data from the terminal with the `gromex` command.

This is an early version, and new features will be added based on user requests and feedback. Feel free to suggest improvements or additional functionality!

## Table of Contents
- [Installation](#installation)
- [Library Usage](#library-usage)
  - [Library Example](#library-example)
  - [Connection Options](#connection-options)
  - [Password Options](#password-options)
  - [Viewing Calendar Summary](#viewing-calendar-summary)
  - [Exporting Calendars](#exporting-calendars)
    - [Export Options](#export-options)
- [Command Line Utility](#command-line-utility)
  - [Command Line Example](#command-line-example)
  - [Command Line Options](#command-line-options)
- [Known Issues](#known-issues)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/rohzb/gromex.git
    cd gromex
    ```

2. Set up the Python environment and install dependencies:

    ```bash
    ./scripts/bootstrap.sh
    ```

## Library Usage

### Library Example

For more detailed examples, refer to [example.ipynb](example.ipynb).

Running the following example will create `.ics` files for all found calendars:

```python
from gromex import GrommunioCalendars

# Step 1: Create an instance of GrommunioCalendars
grommunio = GrommunioCalendars(username="john.doe@helmholtz-berlin.de", autoconnect=False)

# Step 2: Manually connect to the Grommunio CalDAV server
grommunio.connect()

# Step 3: Export calendars to the 'local/cals/' directory
grommunio.export(path='local/cals/')
```

### Connection Options

- **`autoconnect=True`** (default): Automatically connects to the CalDAV server when creating the instance.
  
  ```python
  grommunio = GrommunioCalendars(username="john.doe@helmholtz-berlin.de")  # Automatically connects
  ```

- **`autoconnect=False`**: Requires manually calling the `connect()` method to establish a connection.

  ```python
  grommunio = GrommunioCalendars(username="john.doe@helmholtz-berlin.de", autoconnect=False)
  grommunio.connect()  # Manually connects
  ```

- **Using a Custom Server**: To connect to a different CalDAV server, pass the `url` parameter to the constructor. The default server is `https://hope.helmholtz-berlin.de`, but you can override it like this:

  ```python
  grommunio = GrommunioCalendars(username="john.doe@helmholtz-berlin.de", url="https://custom-server.com")
  ```

  This will connect to the specified server instead of the default.


### Password Options

1. **Pass Password Directly**: Provide the password directly when creating the instance (avoid hardcoding sensitive data).

   ```python
   grommunio = GrommunioCalendars(username="john.doe@helmholtz-berlin.de", password="yourpassword")
   ```

2. **Prompt for Password**: If no password is provided, the system will prompt you to securely input it.

   ```python
   grommunio = GrommunioCalendars(username="john.doe@helmholtz-berlin.de")
   ```

### Viewing Calendar Summary

Use the `show_summary()` method to display a summary of available calendars, including names, supported components (VEVENT, VTODO), and event/task counts.

```python
grommunio.show_summary()  # Displays the summary of available calendars
```

### Exporting Calendars

The `export()` method exports calendar data to a specified directory.

#### Export Options

1. **`save_single_events`** (default: `False`): If `True`, each event is saved as an individual `.ics` file.
2. **`save_combined_calendar`** (default: `True`): If `True`, a combined `.ics` file is saved for the entire calendar.

#### Examples

- **Export only combined calendars** (default):

  ```python
  grommunio.export(path='local/cals/')
  ```

- **Export both individual events and combined calendars**:

  ```python
  grommunio.export(path='local/cals/', save_single_events=True, save_combined_calendar=True)
  ```

## Command Line Utility

The `gromex` command-line utility allows you to export calendar data directly from the terminal.

### Command Line Example:

```bash
gromex [username] [destination] [--server SERVER_URL] [--password PASSWORD] [--save-separate]
```

#### Example Usage:

- Using the default Grommunio server:
  
  ```bash
  gromex username@example.com /path/to/export --save-separate
  ```

- Specifying a custom server:

  ```bash
  gromex username@example.com /path/to/export --server https://example.com --save-separate
  ```

### Command Line Options:

- `username`: Grommunio account username (e.g., `user@example.com`).
- `destination`: Directory to save the exported `.ics` files.
- `--server`: Optional. Specify the CalDAV server URL (default: `https://hope.helmholtz-berlin.de`).
- `--password`: Optional. Provide the password for the Grommunio account. If not provided, it will prompt for input.
- `--save-separate`: Optional. If included, saves each event as a separate `.ics` file.

## Known Issues

1. **Recurring Events Import**:
   - Importing `.ics` files into Exchange has issues with recurring events - they do not show up. That problem is under investigation now...

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
