# gromex (GROMunnio EXport)

`gromex` is a Python module for exporting data from Grommunio. Currently, it supports exporting calendars via the `GrommunioCalendars` class.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/gromex.git
    cd gromex
    ```

2. Set up the Python environment and install dependencies:

    ```bash
    ./scripts/bootstrap.sh
    ```

## Usage

### Example

See [example.ipynb](example.ipynb) for an example.

```python
from gromex import GrommunioCalendars

# Step 1: Create an instance of GrommunioCalendars
grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de", autoconnect=False)

# Step 2: Manually connect to the Grommunio CalDAV server
grommunio.connect()

# Step 3: Export calendars to the 'local/cals/' directory
grommunio.export(path='local/cals/')
```

### Connection Options

#### `autoconnect` Option

- **`autoconnect=True`** (default): Automatically connects to the CalDAV server upon instance creation.

  ```python
  grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de")  # Automatically connects
  ```

- **`autoconnect=False`**: Requires manually calling `connect()` to establish the connection.

  ```python
  grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de", autoconnect=False)
  grommunio.connect()  # Manually connects
  ```

#### Password Options

1. **Pass Password Directly**: Provide the password as an argument (avoid hardcoding sensitive data).

   ```python
   grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de", password="yourpassword")
   ```

2. **Prompt for Password**: If no password is provided, you’ll be securely prompted.

   ```python
   grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de")
   ```

### Viewing Calendar Summary

Use `show_summary()` to display the calendar names, supported components (VEVENT, VTODO), and event/task counts.

```python
grommunio.show_summary()  # Displays the summary of available calendars
```

### Exporting Calendars

The `export()` method exports calendars to the specified directory.

#### Export Options

1. **`save_single_events`** (default: `False`): Saves each event as an individual `.ics` file if `True`.
2. **`save_combined_calendar`** (default: `True`): Saves a combined `.ics` file for the entire calendar.

#### Examples

- **Export combined calendars only (default)**:

  ```python
  grommunio.export(path='local/cals/')
  ```

- **Export both individual events and combined calendars**:

  ```python
  grommunio.export(path='local/cals/', save_single_events=True, save_combined_calendar=True)
  ```

### Parameters Overview

- **`username`**: Grommunio username (e.g., `user@example.com`).
- **`password`**: Optional. If not provided, you'll be prompted securely.
- **`autoconnect`**: Optional. Automatically connects when set to `True`.
- **`export(path)`**: Exports calendar data to the specified directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
