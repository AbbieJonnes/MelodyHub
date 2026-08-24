# MelodyHub

MelodyHub is a desktop music application built with Python and Tkinter. It allows users to discover music, view song information, save songs, manage favorites, and store song data locally using SQLite.

## Features

Browse and search for songs

View song details

Preview music

Save songs locally

Add and remove favorite songs

Update saved song information

Delete saved songs

Prevent duplicate songs from being saved

Store song information using SQLite

Desktop graphical user interface built with Tkinter

## Technologies Used

Python

Tkinter

SQLite

PIL/Pillow

Music API

ReportLab

svglib

Project Structure

MelodyHub/
│
├── main.py
├── ui.py
├── database.py
├── musicapi.py
├── models.py
├── utils.py
└── melodyhub.db

## Database

MelodyHub uses SQLite to store song information locally.

The songs table contains:

ID

Title

Artist

Album

Artwork

Preview URL

Track ID

Favorite status

Installation

Clone the repository:

git clone https://github.com/AbbieJonnes/MelodyHub.git

Move into the project directory:

cd MelodyHub

Create a virtual environment:

python -m venv myenv

Activate the virtual environment on Windows using Git Bash:

source myenv/Scripts/activate

## Install the required dependencies:

pip install -r requirements.txt

## Run the application:

python main.py

## Author

Abigael Mwangi

Email: abigaelmwangi534@gmail.com

GitHub: Abbie Jonnes

## License

This project is licensed under the MIT License.