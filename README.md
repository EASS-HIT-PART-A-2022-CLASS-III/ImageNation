# ImagePlotter

ImagePlotter is a web application built with FastAPI that allows users to upload images and retrieve the GPS coordinates, date, and perceptual hash of each image.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.10 or later
* Pip 21.0 or later
* Docker 19.03 or later
* Docker Compose 1.27 or later

### Installing

1. Clone the repository:

```
git clone https://github.com/EASS-HIT-PART-A-2022-CLASS-III/myImages.git
```

2. Navigate to the project directory:

```
cd imageplotter
```

3. Install the project dependencies:

```
pip install -r requirements.txt
```

4. Build the Docker image:

```
docker build -t imageplotter .
```

### Running

1. Start the Docker container:

```
docker run -p 8800:8800 imageplotter
```

2. Open your web browser and go to http://localhost:8800.


## Usage

- Uploading one or multiple images at once
- Calculating the perceptual hash value (phash) for each uploaded image
- Extracting GPS and date metadata from the EXIF data of each uploaded image
- Displaying the list of uploaded images
- Deleting uploaded images
- Updating metadata for uploaded images
- Finding and displaying duplicate images based on phash value


## API Endpoints

- `GET /`: Displays a welcome message and the available endpoints.
- `POST /images/`: Upload one or multiple images and calculate their phash value and extract GPS and date metadata.
- `GET /images/`: Displays a list of uploaded images.
- `GET /images/{image_name}`: Displays the details of a specific image.
- `DELETE /deleteImage/{image_name}`: Deletes a specific image.
- `PUT /updateImage/{image_name}`: Updates the metadata of a specific image.
- `PATCH /patchImage/{image_name}`: Partially updates the metadata of a specific image.
- `GET /findDuplicateImages`: Finds and displays duplicate images.


## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
* [Docker](https://www.docker.com/) - Containerization platform

## Authors

* **Roy Galili** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.