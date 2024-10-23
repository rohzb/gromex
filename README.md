# gromex (GROMunnio EXport)

`gromex` is a Python module designed for exporting calendars from a Grommunio CalDAV server using the `GrommunioCalendars` class.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Example](#example)
  - [Connection Options](#connection-options)
  - [Password Options](#password-options)
  - [Viewing Calendar Summary](#viewing-calendar-summary)
  - [Exporting Calendars](#exporting-calendars)
    - [Export Options](#export-options)
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

## Usage

### Example

For more detailed examples, refer to [example.ipynb](example.ipynb).

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

- **`autoconnect=True`** (default): Automatically connects to the CalDAV server when creating the instance.
  
  ```python
  grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de")  # Automatically connects
  ```

- **`autoconnect=False`**: Requires manually calling the `connect()` method to establish a connection.

  ```python
  grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de", autoconnect=False)
  grommunio.connect()  # Manually connects
  ```

### Password Options

1. **Pass Password Directly**: Provide the password directly when creating the instance (avoid hardcoding sensitive data).

   ```python
   grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de", password="yourpassword")
   ```

2. **Prompt for Password**: If no password is provided, the system will prompt you to securely input it.

   ```python
   grommunio = GrommunioCalendars(username="ovsyannikov@helmholtz-berlin.de")
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

## Known Issues

1. **Timezone Compatibility**:
   - Some events may raise errors due to Grommunio's incompatibility with iCal time zones:
     ```
     ERROR:root:Ical data was modified to avoid compatibility issues
     (Your calendar server breaks the icalendar standard)
     This is probably harmless, particularly if not editing events or tasks
     (error count: 1 - this error is ratelimited)
     NoneType: None
     ERROR:root:--- 
     +++ 
     @@ -30,7 +30,6 @@
     SUMMARY;LANGUAGE=en-us:NTT meets HZB-AOT
     DTSTART;TZID=W. Europe Standard Time:20240701T110000
     DTEND;TZID=W. Europe Standard Time:20240701T120000
     -DUE;TZID=W. Europe Standard Time:20240626T120000
     CLASS:PUBLIC
     PRIORITY:5
     X-MICROSOFT-CDO-IMPORTANCE:1
     ```
     These errors can be ignored; they don’t affect functionality.

2. **Recurring Events Import**:
   - Importing `.ics` files into Exchange has issues with recurring events - they do not show up. That problem is under investigation now...

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
