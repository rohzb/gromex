import os
import caldav
from caldav.lib.error import AuthorizationError
import getpass  # For safely asking for password
from icalendar import Calendar
from tqdm import tqdm  # For progress bar
from typing import Optional, List

class GrommunioCalendars:
    """
    A class to connect to a Grommunio service via CalDAV, retrieve calendars, and export events.

    This class provides functionalities for connecting to a Grommunio CalDAV service, 
    listing calendars, showing calendar summaries, and exporting calendar events into 
    .ics files (either individually or as a combined calendar file).

    Example Usage:
    --------------
    # Automatically connect and export only combined calendars:
    cal = GrommunioCalendars(username="john.doe") # It will ask for a password
    cal.export(path="/path/to/export/directory")

    # Manual connect and export both individual events and combined calendars:
    cal = GrommunioCalendars(username="john.doe", password="password", autoconnect=False)
    cal.connect()
    cal.export(path="/path/to/export/directory", save_single_events=True, save_combined_calendar=True)

    Class Attributes:
    -----------------
    default_max_retries : int
        The default number of retries for password entry in case of an AuthorizationError.
    
    Parameters:
    -----------
    username : str
        The username for connecting to the Grommunio service.
    password : Optional[str], optional
        The password for the Grommunio service (if not provided, it will prompt).
    url : str, optional
        The CalDAV URL for the Grommunio service (default: "https://hope.helmholtz-berlin.de").
    autoconnect : bool, optional
        Whether to automatically connect on class instantiation (default: True).
    """

    default_max_retries = 3  # Class-level default for max retries

    def __init__(self, username: str, password: Optional[str] = None, 
                 url: str = "https://hope.helmholtz-berlin.de", autoconnect: bool = True) -> None:
        """
        Initializes the GrommunioCalendars class.

        Automatically connects to the Grommunio CalDAV server if `autoconnect=True`. 
        If `password` is not provided, it will prompt for the password.

        Parameters:
        -----------
        username : str
            The username for connecting to the Grommunio service.
        password : Optional[str], optional
            The password for the Grommunio service (if not provided, it will prompt).
        url : str, optional
            The CalDAV URL for the Grommunio service (default: "https://hope.helmholtz-berlin.de").
        autoconnect : bool, optional
            Whether to automatically connect on class instantiation (default: True).
        """
        if not username:
            raise ValueError("The 'username' parameter is required.")
        self.username = username
        self.url = url
        self.__connected = False
        self.principal = None

        self.password = password

        self.calendar_url = f"{self.url}/dav/calendars/{self.username}/Calendar/"

        # Automatically connect if autoconnect is True
        if autoconnect:
            self.connect()

    @property
    def password(self) -> str:
        """
        Get or set the password for the Grommunio service.

        Getter:
        --------
        If the password was not provided during instantiation, this property will 
        prompt the user for the password securely using `getpass.getpass`. Once entered, 
        the password will be stored for future use unless explicitly reset.

        Setter:
        --------
        Setting the password allows you to manually specify or reset the password. If 
        set to `None`, it will prompt for the password again the next time the `password` 
        property is accessed.

        Returns:
        --------
        str:
            The password used for connecting to the Grommunio service.
        """
        if self._password is None:
            self._password = getpass.getpass(prompt="Enter your password: ")
        return self._password

    @password.setter
    def password(self, value: Optional[str]) -> None:
        """
        Set or reset the password for the Grommunio service.

        If set to `None`, the password will be cleared and the user will be prompted 
        for it again the next time the `password` property is accessed.
        """
        self._password = value



    def connect(self, max_retries: Optional[int] = None) -> None:
        """
        Connect to the Grommunio CalDAV server.

        Establishes a connection with the CalDAV server using the provided credentials. 
        If authentication fails, it will prompt for the password again up to max_retries times.

        Parameters:
        -----------
        max_retries : Optional[int], optional
            The maximum number of password retries in case of an AuthorizationError. 
            If not provided, uses the class-level default (`default_max_retries`).

        Raises:
        -------
        ConnectionError:
            If the connection to the CalDAV server fails.
        """
        if max_retries is None:
            max_retries = self.default_max_retries
            
        print("Connecting to Grommunio services...")
        retries = 0
        while retries < max_retries:
            try:
                if not self.principal:
                    self.client = caldav.DAVClient(url=self.calendar_url, username=self.username, password=self.password)
                    self.principal = self.client.principal()
                    print(f"Connected to CalDAV for {self.principal.get_display_name()}.")
                    self.__connected = True
                    break  # Exit loop after successful connection
            except AuthorizationError:
                print("Authorization failed. Please try again.")
                self.password = None
                retries += 1
            except Exception as e:
                raise ConnectionError(f"Failed to connect to CalDAV server: {e}")

        if retries == max_retries:
            raise ConnectionError("Maximum password retries exceeded. Failed to connect to the CalDAV server.")


    @property
    def calendars(self) -> List[caldav.objects.Calendar]:
        """
        Retrieve the list of calendars after connecting.

        Returns:
        --------
        List[caldav.objects.Calendar]:
            The list of calendars available in the CalDAV server.

        Raises:
        -------
        ConnectionError:
            If the connection has not been established.
        """
        if not self.principal:
            raise ConnectionError("Not connected to the server. Call 'connect()' first or use 'autoconnect=True'.")
        return self.principal.calendars()

    def show_summary(self) -> None:
        """
        Show a summary of calendars including their supported components and counts of events and tasks.

        This method prints out the name of each calendar, the supported components (VEVENT and VTODO),
        and the number of events and tasks in each calendar.
        
        Raises:
        -------
        ConnectionError:
            If the connection has not been established.
        """
        if not self.principal:
            raise ConnectionError("Not connected to the server. Call 'connect()' first or use 'autoconnect=True'.")
        
        # Loop through each calendar and display information
        for calendar in self.calendars:
            print(f"Calendar Name: {calendar.name}")

            # Get the supported components for this calendar
            supported_components = calendar.get_supported_components()
            print(f"Supported Components: {supported_components}")

            # Fetching events (VEVENT) and tasks (VTODO) counts
            event_count = len(calendar.events())  # VEVENT (events)
            task_count = len(calendar.todos())    # VTODO (tasks)

            print(f" - VEVENT (Events): {event_count} items")
            print(f" - VTODO (Tasks): {task_count} items")

    def export(self, path: str, save_single_events: bool = False, save_combined_calendar: bool = True) -> None:
        """
        Export all calendars and events to the specified directory.

        Exports all events in the selected calendars to `.ics` files. Optionally, it can export individual 
        event files and/or combined `.ics` files for each calendar.

        Parameters:
        -----------
        path : str
            The base directory to save the exported calendars.
        save_single_events : bool, optional
            Whether to save each event as an individual `.ics` file (default: False).
        save_combined_calendar : bool, optional
            Whether to save a combined `.ics` file for each calendar (default: True).

        Raises:
        -------
        ValueError:
            If the `path` is not provided.
        ConnectionError:
            If the connection has not been established.
        """
        if not path:
            raise ValueError("The 'path' parameter is required.")
        
        if not os.path.exists(path):
            os.makedirs(path)  # Create the base directory if it doesn't exist

        for calendar in self.calendars:
            calendar_name = calendar.name.replace(" ", "_")  # Replace spaces in calendar names with underscores
            calendar_path = os.path.join(path, calendar_name)
            
            if not os.path.exists(calendar_path) and save_single_events:
                os.makedirs(calendar_path)  # Create a directory for each calendar if saving single events

            combined_cal = Calendar()  # For combined calendar
            combined_calendar_path = os.path.join(path, f"{calendar_name}.ics")

            events = calendar.events()  # Fetch all events for the calendar
            # Use tqdm to show progress
            for event in tqdm(events, desc=f"Exporting {calendar.name}"):
                combined_cal.add_component(event.icalendar_component)

                if save_single_events:
                    uid = str(event.icalendar_component['UID'])
                    data = event.data
                    filename = os.path.join(calendar_path, f"{uid}.ics")

                    # Write event data to .ics file
                    with open(filename, 'w') as ics_file:
                        ics_file.write(data)

            if save_combined_calendar:
                # Export the combined .ics file for the calendar
                with open(combined_calendar_path, 'wb') as ics_file:
                    ics_file.write(combined_cal.to_ical())

