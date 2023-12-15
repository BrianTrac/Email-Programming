import shutil
import os
import time

def move_subfolder(source_path, destination_path, subfolder_name):
    # Construct the full paths for the source and destination
    source_folder = os.path.join(source_path, subfolder_name)
    destination_folder = os.path.join(destination_path, subfolder_name)

    try:
        # Ensure all file objects are closed
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    f.close()
        # Add a short delay
        time.sleep(1)
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

def delete_subfolder(path, subfolder_name):
    # Construct the full path for the subfolder
    subfolder_path = os.path.join(path, subfolder_name)

    try:
        # Delete the subfolder
        shutil.rmtree(subfolder_path)
        print(f"Subfolder '{subfolder_name}' deleted successfully.")
    except FileNotFoundError:
        print(f"Subfolder '{subfolder_name}' not found.")
    except Exception as e:
        print(f"Error deleting subfolder '{subfolder_name}': {e}")

# if __name__ == "__main__":
#     source_path = "D:\Python\Email App\Email-Programming-Brian\clientserver@gmail.com\Inbox"
#     destination_path = "D:\Python\Email App\Email-Programming-Brian\clientserver@gmail.com\Trash"
#     subfolder_name = "80"
#
#     move_subfolder(source_path, destination_path, subfolder_name)
