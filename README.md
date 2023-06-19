# MusicSchoolApp

MusicSchoolApp is an API and web application for managing and accessing course and instructor information for a music school. Instructors have a set of instruments they are proficient in, and courses are grouped by instrument and associated with instructors.

This application uses a Python/Flask backend written to PEP8 style guidelines to communicate with a PostgreSQL database, and a Next.js frontend. It integrates with Auth0 for authentication and authorization purposes.

<br>

___

## Getting Started

### Backend

The `./backend` directory contains all of the files for setting up the database and running the Flask server. See the [backend readme](./backend/README.md) for more information.
TODO: integrate Auth0, set up testing

<br>

### Frontend

The `./frontend` directory contains all of the files for running the Next.js frontend, which has client-side authentication with Auth0. See the [frontend readme](./frontend/README.md) for more information.

<br>

___

## Deployment

There is a live version of the app! The backend is available at https://musicschoolapi.onrender.com and the frontend is visible at https://musicschoolapp.onrender.com. Both sides are hosted on free instances at [Render](https://render.com/), so please keep in mind that they spin down after 15 minutes of inactivity and require a few minutes to come back online after a request.

<br>

### Authentication

Authentication of the live version of the app is provided through the Auth0 base domain `xskj.us.auth0.com`. Necessary details for auth setup are provided below.

#### **Obtaining a JWT**

A JWT for API requests can be obtained at the URL https://xskj.us.auth0.com/authorize?udience=musicschool&response_type=token&client_id=IYFMmmLin1gwhdIihoAxY04da5kHqx8Z&redirect_uri=https://musicschoolapp.onrender.com. The URL of the callback page after login will have the JWT embedded in it.

#### **Logging in through the frontend**

Click "login" from the website. After logging in, navigate to the Profile page and the JWT will be displayed at the bottom after "accessToken="