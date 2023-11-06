import shutil
import os
import datetime

def backup_database():
    # Source and destination paths
    source_path = "/home/henne/stratus/database.db"
    archive_folder = "/home/henne/stratus/archive/"

    # Create the archive folder if it doesn't exist
    os.makedirs(archive_folder, exist_ok=True)

    # Generate timestamp for the backup file
    timestamp = datetime.datetime.now().strftime("%d%m%Y")

    # Destination path for the backup file
    backup_filename = f"database_{timestamp}.db"
    destination_path = os.path.join(archive_folder, backup_filename)

    # Copy the database file to the archive folder
    shutil.copy2(source_path, destination_path)

    print(f"copied to {destination_path}")

    # Retrieve a list of all backup files in the archive folder
    backup_files = os.listdir(archive_folder)

    # Sort the backup files by modification time (oldest to newest)
    backup_files.sort(key=lambda x: os.path.getmtime(os.path.join(archive_folder, x)))

    # Remove the oldest backup file if there are more than 7 backups
    if len(backup_files) > 7:
        oldest_backup = os.path.join(archive_folder, backup_files[0])
        os.remove(oldest_backup)

backup_database()