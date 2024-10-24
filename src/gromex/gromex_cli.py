import argparse
from gromex import GrommunioCalendars
import importlib.metadata

def main():
    # Automatically get the version from the module's metadata
    version = importlib.metadata.version('gromex')

    parser = argparse.ArgumentParser(
        description=f"""
        gromex - A tool to export calendar data from Grommunio.
        Export calendars to a specified directory, with an option to save events as separate .ics files.

        Version: {version}
        """,
        epilog="""
        Example:
        gromex username@example.com /path/to/export --save-separate
        gromex username@example.com /path/to/export --password yourpassword --save-separate
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Required arguments
    parser.add_argument('username', type=str, help="Grommunio account username (e.g., user@example.com)")
    parser.add_argument('destination', type=str, help="Directory to save the exported .ics files")

    # Optional arguments
    parser.add_argument('--password', type=str, help="Password for the Grommunio account (optional)")
    parser.add_argument('--save-separate', action='store_true', help="Save each event as a separate .ics file")
    parser.add_argument('--version', action='version', version=f"%(prog)s {version}", help="Show gromex version and exit")

    args = parser.parse_args()

    # Create an instance of GrommunioCalendars using autoconnect
    grommunio = GrommunioCalendars(username=args.username, password=args.password, autoconnect=True)

    # Export calendars
    grommunio.export(path=args.destination, save_single_events=args.save_separate)

    print(f"Export complete. Files saved to {args.destination}")

if __name__ == "__main__":
    main()
