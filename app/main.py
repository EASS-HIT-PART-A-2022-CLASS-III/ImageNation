from PIL import Image
import os
import hashlib

def calculate_hash(image_path):
    with open(image_path, 'rb') as f:
        # Read the image data
        image_data = f.read()
        # Calculate the MD5 hash of the image data
        hash_value = hashlib.md5(image_data).hexdigest()
    return hash_value

def find_duplicates(folder):
    # Dictionary to store image hashes and their file paths
    hash_dict = {}
    # Loop through all the files in the folder
    for root, dirs, files in os.walk(folder):
        for file in files:
            # Check if the file is an image
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                # Calculate the hash of the image
                image_path = os.path.join(root, file)
                hash_value = calculate_hash(image_path)
                # Check if the hash is already in the dictionary
                if hash_value in hash_dict:
                    # If the hash is already in the dictionary, add the file path to the list
                    hash_dict[hash_value].append(image_path)
                else:
                    # If the hash is not in the dictionary, add it with the file path
                    hash_dict[hash_value] = [image_path]
    
    # Loop through the hash dictionary and print the duplicate images
    for key, value in hash_dict.items():
        if len(value) > 1:
            print(f"Duplicate images found for hash value: {key}")
            for image_path in value:
                print(image_path)

# Example usage
folder_path = "path/to/folder"
find_duplicates(folder_path)