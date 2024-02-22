# Scraper for FreeImages Platform

This project is a Python-based web scraper that utilizes Selenium to automate the process of extracting image URLs from the FreeImages platform based on a specified search term. The URLs are stored in a SQLite database for easy access and management. This tool is particularly useful for collecting a large dataset of image URLs for research, machine learning projects, or personal use.

## Getting Started

These instructions will guide you through setting up and running the scraper on your local machine.

### Installation

To install the environment, simply type the following commands at the terminal

```bash
conda env create -f environment.yml
conda activate selenium-freeimages
```

### Usage

To start scraping images, you can use the following commands:

Basic execution (extracts 1000 URLs of dog images and stores them in the default database):
```bash
python -m main_script
```

Flexible execution (allows you to specify the number of images, database path, and search term):
```bash
python -m main_script --n_images {number} --db_path {path/to/database.db} --search_term {search_term}
```
Replace {number}, {path/to/database.db}, and {search_term} with your desired values.

Examples

Extract 500 cat images and store them in ./data/images.db:
```bash
python -m main_script --n_images 500 --db_path ./data/images.db --search_term cats

```
