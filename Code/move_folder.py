import shutil
import os

def move_subfolder(source_path, destination_path, subfolder_name):
    # Construct the full paths for the source and destination
    source_folder = os.path.join(source_path, subfolder_name)
    destination_folder = os.path.join(destination_path, subfolder_name)

    try:
        # Move the subfolder to the new location
        shutil.move(source_folder, destination_folder)
        print(f"Subfolder '{subfolder_name}' moved successfully.")
    except FileNotFoundError:
        print(f"Subfolder '{subfolder_name}' not found in the source folder.")
    except Exception as e:
        print(f"Error moving subfolder '{subfolder_name}': {e}")

def copy_subfolder(source_path, destination_path, subfolder_name):
    # Construct the full paths for the source and destination
    source_folder = os.path.join(source_path, subfolder_name)
    destination_folder = os.path.join(destination_path, subfolder_name)

    try:
        # Copy the subfolder to the new location
        shutil.copytree(source_folder, destination_folder)
        print(f"Subfolder '{subfolder_name}' copied successfully.")
    except FileNotFoundError:
        print(f"Subfolder '{subfolder_name}' not found in the source folder.")
    except FileExistsError:
        print(f"Subfolder '{subfolder_name}' already exists in the destination folder.")
    except Exception as e:
        print(f"Error copying subfolder '{subfolder_name}': {e}")

# source_path = "D:\Python\Socket Programming\Email\Inbox"
# destination_path = "D:\Python\Socket Programming\Email\Star"
# subfolder_name = "58"

# copy_subfolder(source_path, destination_path, subfolder_name)
