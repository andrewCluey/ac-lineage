# Databricks Permissions Viewer - Lakehouse App

The Databricks Permissions Viewer is a web application designed to simplify the visualization and management of recursive permissions in Databricks. Built with a Vue 3 front end and a FastAPI back end, this app provides an intuitive interface for exploring and analyzing permissions. A workflow to crawl and retrieve permissions data is required to populate the app.

## Features
- **Recursive Permissions Visualization**: Easily view and analyze permissions across Databricks resources.
- **Workflow Integration**: Requires a permissions crawling workflow to gather and process data.
- **Interactive Web Interface**: Built with Vue 3 for a seamless user experience.
- **FastAPI Back End**: Provides a robust and efficient back-end service for data handling.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Environment Variables](#environment-variables)
4. [Running the App](#running-the-app)
5. [Building the Front End for Production](#building-the-front-end-for-production)
6. [Technologies Used](#technologies-used)
7. [Front-End Setup](#front-end-setup)

---

## Installation

### Back-End Setup
1. Ensure Python is installed (preferably in a virtual environment).
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Front-End Setup
1. Navigate to the `front-end` directory:

   ```bash
   cd front-end
   ```

2. Install the dependencies:

   ```bash
   npm install
   ```

---

## Usage

### Back-End
The back end is responsible for processing permissions data retrieved by the crawling workflow. Once the workflow has populated the necessary data, the back end serves it to the front end for visualization.

### Front-End
The front end provides an interactive interface for exploring permissions data. Users can navigate through the recursive structure of permissions and analyze access levels across resources.

---

## Environment Variables

Before running the app, ensure the following environment variables are set in a `.env` file or directly in your environment:

- `DATABRICKS_HOST`: Your Databricks server hostname.
- `DATABRICKS_TOKEN`: Your Databricks access token for authentication.
- `DATABRICKS_WAREHOUSE_PATH`: The HTTP path for your Databricks SQL warehouse.
- `ENV`: Set to `local` for development mode.

Example `.env` file:

```bash
DATABRICKS_HOST=your-databricks-hostname
DATABRICKS_TOKEN=your-access-token
DATABRICKS_WAREHOUSE_PATH=your-http-path
ENV=local
```

---

## Running the App

### Back-End
Start the back-end server with the following command:

```bash
uvicorn app:app --reload
```

This will launch the FastAPI server, typically accessible at `http://127.0.0.1:8000`.

### Front-End
To run the front end in development mode:

1. Navigate to the `front-end` directory:

   ```bash
   cd front-end
   ```

2. Start the development server:

   ```bash
   npm run dev
   ```

The front end will be accessible at `http://localhost:3000`.

---

## Building the Front End for Production

To build the front end for production:

1. Navigate to the `front-end` directory:

   ```bash
   cd front-end
   ```

2. Run the build command:

   ```bash
   npm run build
   ```

3. The static files will be generated in the `dist` folder. These files can be hosted using any static file server or integrated with the back end.

---

## Technologies Used

- **FastAPI**: A modern Python framework for building APIs.
- **Vue 3**: A progressive JavaScript framework for building user interfaces.
- **Vite**: A fast build tool for modern web projects.
- **Python**: The core programming language for the back end.

---

## Front-End Setup

### Recommended IDE Setup
- [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

### Customize Configuration
See [Vite Configuration Reference](https://vite.dev/config/).
