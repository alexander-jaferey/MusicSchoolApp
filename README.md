# MusicSchoolApp

MusicSchoolApp is an API and web application for managing and accessing course and instructor information for a music school. Instructors have a set of instruments they are proficient in, and courses are grouped by instrument and associated with instructors.

This application uses a Python/Flask backend written to PEP8 style guidelines to communicate with a PostgreSQL database, and a Next.js frontend. It integrates with Auth0 for authentication and authorization purposes.

<br>

___

## Getting Started

### Backend

The `./backend` directory contains all of the files for setting up the database and running the Flask server. See the [backend readme](./backend/README.md) for more information.

<br>

### Frontend

The `./frontend` directory contains all of the files for running the Next.js frontend, which has client-side authentication with Auth0. See the [frontend readme](./frontend/README.md) for more information.

<br>

___

## Deployment

There is a live version of the app! The backend is available at https://musicschoolapi.onrender.com and the frontend is visible at https://musicschoolapp.onrender.com. Both sides are hosted on free instances at [Render](https://render.com/), so please keep in mind that they spin down after 15 minutes of inactivity and require a few minutes to come back online after a request.