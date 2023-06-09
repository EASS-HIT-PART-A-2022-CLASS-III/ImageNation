# ImageNation

ImageNation is a web application that enables users to upload images and extract insightful metadata, such as GPS coordinates, date, and perceptual hash. Additionally, it facilitates image management by displaying, updating, and deleting image records. The application is built in Python using FastAPI, Streamlit and Docker for a seamless and efficient user experience.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine

### Prerequisites

- Docker 19.03 or later

### Installing

To run this project, you will need to follow this steps:

1. Clone the repository:

```bash
git clone https://github.com/EASS-HIT-PART-A-2022-CLASS-III/ImageNation.git
```
Navigate to the project directory:

```bash
cd ImageNation/app
```

Use Docker Compose to build and start the project:

```bash
docker-compose up
```

Open your web browser and navigate to http://localhost:8501.
Enjoy :)

Features

    📁 Bulk or single image uploading
    🔍 Perceptual hash calculation for uploaded images
    🌍 GPS coordinates and date metadata extraction from EXIF data
    🖼 Display and management of image records
    🗑 Easy deletion of uploaded images
    🔄 Metadata updates for uploaded images
    🔍 Finding and displaying duplicate images based on perceptual hash values

<!-- Project Architecture
<p align="center">
  <img src="path_to_your_architecture_image" alt="ImagePlotter Architecture"/>
</p> -->
## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
* [Docker](https://www.docker.com/) - Containerization platform
* [Streamlit](https://streamlit.io/) - The Clients side 

## Authors

* **Roy Galili** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.