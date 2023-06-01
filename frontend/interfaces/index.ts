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
  success: boolean
  instrument_id?: string
  instrument?: string
  instructors?: IndexedStringList
  courses?: IndexedStringList
  error?: number
  message?: string
}

export type Instructor = {
  success: boolean
  instructor_id?: string
  name?: string
  workdays?: Weekdays[]
  instruments?: IndexedStringList
  courses_taught?: IndexedStringList
  error?: number
  message?: string
}

export type Course = {
  success: boolean
  id?: string
  course_title?: string
  instrument?: {id: string, name: string}
  schedule?: Weekdays[]
  instructors?: IndexedStringList
  error?: number
  message?: string
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

export type DecodedJwt = {
  iss: string
  sub: string
  aud: string[]
  iat: string
  exp: string
  azp: string
  scope: string
  permissions: string[]
}

export type Deleted = {
  success: boolean
  deleted?: number
  error?: number
  message?: string
}

export enum Weekdays {
  Sun = "Sun",
  Mon = "Mon",
  Tue = "Tue",
  Wed = "Wed",
  Thu = "Thu",
  Fri = "Fri",
  Sat = "Sat"
}