# MusicSchool API

## Introduction

The MusicSchool API is a RESTful API that allows interaction with the music school database of instruments, instructors, and courses. It serves endpoints used by the frontend of the MusicSchoolApp, and is integrated with Auth0 for user authentication and authorization of protected endpoints.

<br>

The API is built around resource-oriented URLS. It accepts standard form-encoded request bodies, returns responses in JSON format, and uses standard HTTP methods and response codes.

<br>

___

## Getting Started

The API runs locally after being setup as explained in [the backend readme](../README.md#getting-started).

**TODO**: set up public deployment and authentication

___

## Error Handling

The API returns JSON objects with standard HTTP response codes for all requests. Unsuccessful requests will have a code in the `4xx` range. Errors are returned with the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

<br>

___

## Endpoints

These are the endpoints available for interaction:

### GET /instruments

Returns a dictionary of instruments, a total instruments count, a total page count, a current page marker, and a success value. Results are paginated in groups of 10 by default, but a `per_page` query argument can be appended to the URL to specify a different grouping size. A `page` query argument can be used to specify a page number.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/instruments
```

#### **SAMPLE RESPONSE**
```
{
    "current_page": 1,
    "instruments": {
        "1": "Guitar",
        "2": "Bass",
        "3": "Drums",
        "4": "Piano",
        "5": "Vocals",
        "6": "Banjo",
        "7": "Mandolin",
        "8": "Saxophone",
        "9": "Trumpet",
        "12": "Clarinet"
    },
    "success": true,
    "total_instruments": 11,
    "total_pages": 2
}
```

### GET /instructors

Returns a dictionary of instructors, a total instructors count, a total page count, a current page marker, and a success value. Results are paginated in groups of 8 by default, but a `per_page` query argument can be appended to the URL to specify a different grouping size. A `page` query argument can be used to specify a page number.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/instructors
```

### ***SAMPLE RESPONSE**
```
{
    "current_page": 1,
    "instructors": {
        "1": {
            "instructor": "Jimi Hendrix",
            "instruments": [
                "Guitar",
                "Vocals"
            ]
        },
        "2": {
            "instructor": "Rosetta Tharpe",
            "instruments": [
                "Guitar"
            ]
        },
        "3": {
            "instructor": "Charlie Christian",
            "instruments": [
                "Guitar"
            ]
        },
        "4": {
            "instructor": "Tosin Abasi",
            "instruments": [
                "Guitar"
            ]
        },
        "5": {
            "instructor": "Jack White",
            "instruments": [
                "Guitar",
                "Vocals",
                "Mandolin"
            ]
        },
        "6": {
            "instructor": "Jaco Pastorius",
            "instruments": [
                "Bass"
            ]
        },
        "7": {
            "instructor": "Tina Weymouth",
            "instruments": [
                "Bass"
            ]
        },
        "8": {
            "instructor": "Paul Mccartney",
            "instruments": [
                "Guitar",
                "Bass",
                "Drums",
                "Piano",
                "Vocals"
            ]
        }
    },
    "success": true,
    "total_instructors": 31,
    "total_pages": 4
```

### GET /courses

Returns a dictionary of courses (sorted by instrument), a total instruments count, a total page count, a current page marker, and a success value. Results are paginated *by instrument* in groups of 5 by default, but a `per_page` query argument can be appended to the URL to specify a different grouping size. A `page` query argument can be used to specify a page number.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/courses
```

#### **SAMPLE RESPONSE**
```
{
    "courses": {
        "Bass": {
            "5": "Beginner Bass",
            "6": "Advanced Bass",
            "7": "Jazz Bass"
        },
        "Drums": {
            "8": "Beginner Drums",
            "9": "Advanced Drums",
            "10": "Jazz Drums"
        },
        "Guitar": {
            "1": "Beginner Guitar",
            "2": "Advanced Guitar",
            "3": "Jazz Guitar",
            "4": "Blues Guitar"
        },
        "Piano": {
            "11": "Beginner Piano",
            "12": "Classical Piano",
            "13": "Jazz Piano"
        },
        "Vocals": {
            "14": "Beginner Vocals",
            "15": "Advanced Vocals",
            "16": "Jazz Vocals"
        }
    },
    "current_page": 1,
    "success": true,
    "total_instruments": 11,
    "total_pages": 3
}
```

### GET /instruments/\<id\>

Returns an instrument name, an instrument ID, a dictionary of associated instructors with IDs and names, a dictionary of associated courses with IDs and names, and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `get:instruments` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/instruments/1
```

#### **SAMPLE RESPONSE**

```
{
    "courses": {
        "1": "Beginner Guitar",
        "2": "Advanced Guitar",
        "3": "Jazz Guitar",
        "4": "Blues Guitar"
    },
    "instructors": {
        "1": "Jimi H",
        "2": "Rosetta T",
        "3": "Charlie C",
        "4": "Tosin A",
        "5": "Jack W",
        "8": "Paul M",
        "35": "Ian A",
        "36": "Kim D"
    },
    "instrument": "Guitar",
    "instrument_id": 1,
    "success": true
}
```

### GET /instructors/\<id\>

Returns an instructor name, an instructor ID, a list of workdays, a dictionary of associated instruments with IDs and names, a dictionary of taught courses with IDs and names, and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `get:instructors` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/instructors/1
```

#### **SAMPLE RESPONSE**

```
{
    "courses_taught": {
        "1": "Beginner Guitar",
        "2": "Advanced Guitar"
    },
    "instructor_id": 1,
    "instruments": {
        "1": "Guitar",
        "5": "Vocals"
    },
    "name": "Jimi Hendrix",
    "success": true,
    "workdays": [
        "Sun",
        "Tue",
        "Wed",
        "Thu"
    ]
}
```

### GET /courses/\<id\>

Returns a course title, a course ID, an associated instrument, a schedule in list format, a dictionary of associated instructors with IDs and names, and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `get:courses` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/courses/1
```

#### **SAMPLE RESPONSE**

```
{
    "course_title": "Beginner Guitar",
    "id": 1,
    "instructors": {
        "1": "Jimi H",
        "2": "Rosetta T",
        "5": "Jack W",
        "35": "Ian A"
    },
    "instrument": {
        "id": 1,
        "name": "Guitar"
    },
    "schedule": [
        "Sun",
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat"
    ],
    "success": true
}
```

### DELETE /instruments/\<id\>

Deletes the instrument with the given ID, if it exists. Returns the deleted instrument's ID and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `delete:instruments` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X DELETE http://127.0.0.1:5000/instruments/10
```

#### **SAMPLE RESPONSE**

```
{
    "deleted": 10,
    "success": true
}
```

### DELETE /instructors/\<id\>

Deletes the instructor with the given ID, if it exists. Returns the deleted instructor's ID and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `delete:instructors` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X DELETE http://127.0.0.1:5000/instructors/10
```

#### **SAMPLE RESPONSE**

```
{
    "deleted": 10,
    "success": true
}
```

### DELETE /courses/\<id\>

Deletes the course with the given ID, if it exists. Returns the deleted course's ID and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `delete:courses` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" -X DELETE http://127.0.0.1:5000/courses/10
```

#### **SAMPLE RESPONSE**

```
{
    "deleted": 10,
    "success": true
}
```

### POST /instruments

Uploads a new instrument. The request should be sent with a body containing an instrument attribute, and optionally containing an instructors attribute. The instructors attribute should only contain the names of instructors already in the database. Returns the uploaded instrument's ID and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `post:instruments` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"instrument":"Upright Bass", "instructors':["Jaco Pastorius", "Paul Mccartney"]}' \
     http://127.0.0.1:5000/instruments
```

#### **SAMPLE RESPONSE**

```
{
    "id": 18,
    "success": true
}
```

### POST /instructors

Uploads a new instrument. The request should be sent with a body containing first and last name attributes, a workdays attribute, and an instruments attribute; and optionally containing a courses attribute. The instruments and courses attributes should only contain the names of instruments and courses already in the database. Returns the uploaded instructor's ID and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `post:instructors` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"first_name":"Nancy", "last_name":"Wilson", "workdays":["Mon", "Wed", "Thu", "Sat"], "instruments':["Guitar"], "courses":["Basic Guitar", "Advanced Guitar"]}' \
     http://127.0.0.1:5000/instructors
```

#### **SAMPLE RESPONSE**

```
{
    "id": 37,
    "success": true
}
```

### POST /courses

Uploads a new course. The request should be sent with a body containing a title attribute, a schedule attribute, and an instrument attribute; and optionally containing an instructors attribute. The instrument and instructors attributes should only contain the names of instruments and instructors already in the database. Returns the uploaded course's ID and a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `post:courses` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"title":"Flamenco Guitar", "instrument":"Guitar", "Schedule":["Sun", "Mon", "Thu", "Fri"], "instructors":["Charlie Christian", "Tosin Abasi"]}' \
     http://127.0.0.1:5000/courses
```

#### **SAMPLE RESPONSE**

```
{
    "id": 37,
    "success": true
}
```

### PATCH /instruments/\<id\>

Modifies an existing instrument. The request should be sent with a body containing any combination of the attributes used for a `POST /instruments` request. Unused attributes will not be changed. Returns a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `patch:instruments` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -X PATCH \
     -d '{"instrument":"Lute", "instructors':["Jack White", "John Paul Jones"]}' \
     http://127.0.0.1:5000/instruments/7
```

#### **SAMPLE RESPONSE**

```
{
    "success": true
}
```

### PATCH /instructors/\<id\>

Modifies an existing instructor. The request should be sent with a body containing any combination of the attributes used for a `POST /instructors` request. Unused attributes will not be changed. Returns a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `patch:instructors` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -X PATCH \
     -d '{"first_name":"Kermit The", "instruments':["Banjo", "Vocals", "Guitar"]}' \
     http://127.0.0.1:5000/instructors/21
```

#### **SAMPLE RESPONSE**

```
{
    "success": true
}
```

### PATCH /courses/\<id\>

Modifies an existing course. The request should be sent with a body containing any combination of the attributes used for a `POST /courses` request, other than the instrument attribute which cannot be changed. Unused attributes will not be changed. Returns a success value. Requests to this endpoint must include an Authorization header with a JWT Bearer token that has the `patch:courses` permission.

#### **SAMPLE REQUEST**

```
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -X PATCH \
     -d '{"instructors":["Ella Fitzgerald", "Ariana Grande", "Billy Joel", "Pete Seeger", "Paul Mccartney"]}' \
     http://127.0.0.1:5000/courses/15
```

#### **SAMPLE RESPONSE**

```
{
    "success": true
}
```