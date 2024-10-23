import os
import caldav
import getpass  # For safely asking for password
from icalendar import Calendar,Event

class Grommunio:
    def __init__(self, user=None, password=None, url="https://hope.helmholtz-berlin.de"):
        if not user:
            raise ValueError("The 'user' parameter is required.")
        self.user = user
        self.url = url
        self.__connected = False
        
        if password is None:
            # Safely ask for the password if not provided
            password = getpass.getpass(prompt="Enter your password: ")
        self.password = password

    def connect(self):
        """ Placeholder for Grommunio-specific connection logic. """
        if not self.__connected:
            print("Connecting to Grommunio services...")
            self.__connected = True
            # Placeholder logic for Grommunio-specific connection steps.

class Calendars(Grommunio):
    def __init__(self, url=None, username=None, password=None, autoconnect=True):
        if not url:
            url = "https://hope.helmholtz-berlin.de"  # Use default URL if not provided
        super().__init__(user=username, password=password, url=url)
        self.calendar_url = f"{self.url}/dav/calendars/{self.user}/Calendar/"
        self.principal = None

        # Automatically connect if autoconnect is True
        if autoconnect:
            self.connect()

    def connect(self):
        """ Automatically connect to the CalDAV server and Grommunio services. """
        if not self.principal:
            try:
                super().connect()  # Call the parent connect method for Grommunio
                self.client = caldav.DAVClient(url=self.calendar_url, username=self.user, password=self.password)
                self.principal = self.client.principal()
                print(f"Connected to CalDAV for {self.principal.get_display_name()}.")
            except Exception as e:
                raise ConnectionError(f"Failed to connect to CalDAV server: {e}")

    @property
    def calendars(self):
        """ Retrieve the list of calendars after connecting. """
        if not self.principal:
            raise ConnectionError("Not connected to the server. Call 'connect()' first or use 'autoconnect=True'.")
        return self.principal.calendars()

    def show_summary(self):
        """ Show a summary of calendars including their supported components and counts of events. """
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

    def export(self, path=None):
        """ Export all calendars and events to the specified directory. """
        if not path:
            raise ValueError("The 'path' parameter is required.")
        
        if not os.path.exists(path):
            os.makedirs(path)  # Create the base directory if it doesn't exist

        for calendar in self.calendars:
            calendar_name = calendar.name.replace(" ", "_")  # Replace spaces in calendar names with underscores
            calendar_path = os.path.join(path, calendar_name)
            
            combined_cal = Calendar()
            combined_calendar_path = os.path.join(path, f"{calendar_name}.ics")

            if not os.path.exists(calendar_path):
                os.makedirs(calendar_path)  # Create a directory for each calendar

            events = calendar.events()  # Fetch all events for the calendar
            for event in events:
                combined_cal.add_component(event.icalendar_component)
                uid = str(event.icalendar_component['UID'])
                data = event.data
                filename = os.path.join(calendar_path, f"{uid}.ics")

                # Write event data to .ics file
                with open(filename, 'w') as ics_file:
                    ics_file.write(data)


                print(f"Exported event {uid} to {filename}")
            
            with open(combined_calendar_path, 'wb') as ics_file:
                    ics_file.write(combined_cal.to_ical())
            


# Example usage with autoconnect (default):
# cal = Calendars(username="john.doe", password="password")
# cal.show_summary()

# Example usage with manual connect:
# cal = Calendars(username="john.doe", password="password", autoconnect=False)
# cal.connect()
# cal.show_summary()
