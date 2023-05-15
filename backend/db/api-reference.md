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

Returns a dictionary of instruments and a success value. Results are paginated in groups of 10, and a page argument can be appended to the URL to specify a page number.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/instruments
```

#### **SAMPLE RESPONSE**
```
{
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
    "success": true
}
```

### GET /instructors

Returns a dictionary of instructors and a success value. Results are paginated in groups of 10, and a page argument can be appended to the URL to specify a page number.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/instructors
```

### ***SAMPLE RESPONSE**
```
{
    "instructors": {
        "1": {
            "instructor": "Jimi H",
            "instruments": [
                "Guitar",
                "Vocals"
            ]
        },
        "2": {
            "instructor": "Rosetta T",
            "instruments": [
                "Guitar"
            ]
        },
        "3": {
            "instructor": "Charlie C",
            "instruments": [
                "Guitar"
            ]
        },
        "4": {
            "instructor": "Tosin A",
            "instruments": [
                "Guitar"
            ]
        },
        "5": {
            "instructor": "Jack W",
            "instruments": [
                "Guitar",
                "Vocals",
                "Mandolin"
            ]
        },
        "6": {
            "instructor": "Jaco P",
            "instruments": [
                "Bass"
            ]
        },
        "7": {
            "instructor": "Tina W",
            "instruments": [
                "Bass"
            ]
        },
        "8": {
            "instructor": "Paul M",
            "instruments": [
                "Guitar",
                "Bass",
                "Drums",
                "Piano",
                "Vocals"
            ]
        },
        "9": {
            "instructor": "John Paul J",
            "instruments": [
                "Bass",
                "Piano",
                "Mandolin"
            ]
        },
        "10": {
            "instructor": "Ringo S",
            "instruments": [
                "Drums",
                "Vocals"
            ]
        }
    },
    "success": true
}
```

### GET /courses

Returns a dictionary of courses, sorted by instrument, and a success value. Results are paginated *by instrument* in groups of 5, and a page argument can be appended to the URL to specify a page number.

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
    "success": true
}
```