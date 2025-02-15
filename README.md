![Screenshot 2024-07-02 184144](https://github.com/LookslikeLenni/uni-face-recognition/assets/93777813/cdd1a809-4f1a-4302-a23b-bddab5cc062a)
![Screenshot 2024-07-02 184226](https://github.com/LookslikeLenni/uni-face-recognition/assets/93777813/6dd95775-2c35-45f2-866f-1de007c6dc3e)
![Screenshot 2024-07-02 184433](https://github.com/LookslikeLenni/uni-face-recognition/assets/93777813/3a8742aa-ffe8-4e0f-81ae-c01e88b83b71)
![Screenshot 2024-07-02 184304](https://github.com/LookslikeLenni/uni-face-recognition/assets/93777813/9a2507a7-2291-4a9e-b9a6-04abf09d0ba1)



# Facial Recognition API

This FastAPI application utilizes advanced face recognition techniques combined with a robust back-end system to manage user data and images. It supports a variety of operations, including user creation, image uploading, and retrieval of user details, making it versatile for applications requiring biometric functionality.
DeepFace is used for running the Face models and encoding Face Images (a GPU is required)

## Installation and Setup

### Prerequisites

Ensure you have Python 3.6+ installed on your system. You also need to have pip available for installing Python packages. Moreover you need Cmake. If you use VSCode ensure you have the C++ support installed.

### Installing Dependencies

Install all necessary Python packages by running the following command:

    pip install fastapi uvicorn sqlalchemy opencv-python opencv-python-headless numpy python-multipart cmake jinja2 deepface tf-keras {tensorflow, tensorflow-metal or tensorflow-gpu} tqdm

These packages include FastAPI for the web framework, Uvicorn for serving the application, SQLAlchemy for database operations, OpenCV for image processing, and other supporting libraries.

### Database Setup

This application uses SQLite as the database, which is a lightweight disk-based database that does not require a separate server process. The database file (`user.db`) will be created in your project directory automatically upon running the application if it does not already exist.

## Running the Application

To start the server, use the following command:

    python3 backend

To reload all the embeddings, use the following argument:

    python3 backend -r


## API Endpoints

Below are the provided endpoints along with how to use them effectively:

### `POST /users/`

**Description:** Adds a new user with the provided first name, last name, and greeting.

**Usage:** Send a JSON object with `first_name`, `last_name`, and `greeting`.

### `POST /users/{user_id}/images/`

**Description:** Uploads and stores an image to the specified user's profile.

**Usage:** Form-data with `image_file` field containing the image file.

### `DELETE /users/{user_id}/`

**Description:** Deletes the specified user from the database along with all associated images.

**Usage:** Specify the `user_id` in the URL.

### `GET /users/`

**Description:** Retrieves a list of all registered users.

**Usage:** Direct GET request to fetch data.

### `GET /users/{user_id}/`

**Description:** Fetches detailed information about a specific user by `user_id`.

**Usage:** Include `user_id` in the URL.

### `DELETE /users/{user_id}/images/`

**Description:** Removes an indexed image from a user's profile.

**Usage:** Provide `user_id` and specify the `image_index` to remove.

### `GET /users/{user_id}/images/zip/`

**Description:** Downloads all images for a specified user compressed into a ZIP file.

**Usage:** Provide the `user_id`.

### `PUT /users/{user_id}/`

**Description:** Updates details for a specified user.

**Usage:** Send a JSON object with any updated user fields.

### `GET /users/{user_id}/images/{image_index}/`

**Description:** Retrieves a specific image from a user's collection by index.

**Usage:** Specify both `user_id` and `image_index`.

### `GET /timetogether/{user1}/{user2}/`

**Description:** Retrieves the time the two users have spend in frame together.

**Usage:** Specify `user1`, `user2` and retrieve a float in seconds.

### `GET /time/{user_id}/`

**Description:** Retrieves a specific user's time he has spend in frame.

**Usage:** Specify `user_id` and retrieve a float in seconds.

### `GET /compare/{user_id_1}/{user_id_2}/`

**Description:** compare the first image of each user returning 0-1 how similar they are

**Usage:** Provide the `user_id_1` and `user_id_2`

### `GET /export/`

**Description:** Export the Table with `ID, FISTNAME, LASTNAME, IMAGEID, IMAGEDATA` as a python friendly csv

**Usage:** Connect to this endpoint from a client.

### `GET /current/`

**Description:** Retrieves all users that are currently in frame.

**Usage:** Connect to this endpoint from a client.

### `GET /video_feed`

**Description:** Streams a live video feed that is processed to detect and recognize faces.

**Usage:** Connect to this endpoint from a client that supports video streaming.

### `GET /`

**Description:** Serves the homepage of the application.

**Usage:** Access this endpoint from any web browser to view the homepage.

## Conclusion

This README provides all the necessary details to get the application up and running, and to understand how to interact with its comprehensive suite of endpoints. For production environments, consider additional security, performance optimization, and error handling mechanisms.

