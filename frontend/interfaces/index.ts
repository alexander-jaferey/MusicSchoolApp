export type User = {
  email: string
  email_verified: boolean
  name: string
  nickname: string
  picture: string
  sub: string
  updated_at: string
}

export type Instrument = {
  instrument: string
  instructors: string[]
}

export type Instructor = {
  first_name: string
  last_name: string
  workdays: string[]
  instruments: string[]
  courses: string[]
}

export type Course = {
  title: string
  instrument: string
  schedule: string[]
  instructors: string[]
}

export type InstructorInfo = {
  instructor: string
  instruments: string[]
}

export type IndexedStringList = {
  [index: string]: string
}

export type IndexedInstructorList = {
  [index: string]: InstructorInfo
}

export type IndexedCourseList = {
  [index: string]: IndexedStringList
}