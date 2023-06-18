import { useRouter } from "next/router";
import {
  Course,
  IndexedInstructorList,
  IndexedStringList,
  Weekdays,
} from "../interfaces";
import { alertService } from "../services";

type InstrumentFormProps = {
  method: string;
  instruments?: IndexedStringList;
  instructors: IndexedInstructorList;
  values?: Course;
};

const CourseForm = ({
  method,
  instruments,
  instructors,
  values,
}: InstrumentFormProps) => {
  const router = useRouter();
  const handleSubmit = async (e) => {
    e.preventDefault();
    const title = e.target.title.value;
    const scheduleOptions = e.target.weekday;
    const instructorOptions = e.target.instructor;
    const instrumentOptions = e.target.instrument;

    let selectedDays = [];
    let selectedInstructors = [];
    let instrument = [];

    for (let i = 0; i < scheduleOptions.length; i++) {
      if (scheduleOptions[i].checked) {
        selectedDays.push(scheduleOptions[i].value);
      }
    }

    for (let i = 0; i < instructorOptions.length; i++) {
      if (instructorOptions[i].checked) {
        selectedInstructors.push(instructorOptions[i].value);
      }
    }

    for (let i = 0; i < instrumentOptions.length; i++) {
      if (instrumentOptions[i].checked) {
        instrument.push(instrumentOptions[i].value);
        break;
      }
    }

    const data = {
      title: title,
      instrument: instrument[0],
      schedule: selectedDays,
      instructors: selectedInstructors,
    };
    const json = JSON.stringify(data);
    console.log(json);

    const request = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: json,
    };

    const queryParams =
      method === "PATCH" ? `entity=courses&id=${values.id}` : "entity=courses";

    const response = await fetch(`/api/submit?${queryParams}`, request);
    const result = await response.json();

    const action = method === "PATCH" ? "update" : "add";

    if (result.error) {
      const error = result.error;
      const errorMessage = result.message;

      alertService.error(
        `Could not ${action} course (error ${error}: ${errorMessage})`,
        { id: "main" }
      );
    } else {
      alertService.success(`Course ${action}ed`);
      setTimeout(function () {
        router.push("/");
      }, 1000);
    }
  };

  const scheduleArray = values ? values.schedule : [];
  const instructorsArray = values ? Object.keys(values.instructors) : [];

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="title" className="text-xl">
        Title
      </label>
      {values ? <div>Current: {values.course_title}</div> : <></>}
      <br />
      <input type="text" name="title" id="title" className="mb-3" />
      <fieldset className="mb-2">
        <legend className="text-xl">Schedule</legend>
        <div className="max-h-36 max-w-fit overflow-y-scroll">
          {Object.values(Weekdays).map((weekday) => (
            <>
              <input
                type="checkbox"
                name="weekday"
                id="weekday"
                key={weekday}
                value={weekday}
                defaultChecked={
                  scheduleArray.includes(weekday) ? true : false
                }
              />
              <label
                key={`${weekday}-label`}
                htmlFor={weekday}
                className="px-2"
              >
                {weekday}
              </label>
              <br />
            </>
          ))}
        </div>
      </fieldset>
      <fieldset>
        <legend className="text-xl">Instrument</legend>
        {values ? <div>Current: {values.instrument.name}</div> : <></>}
        <div className="max-h-36 max-w-fit overflow-y-scroll">
          {Object.entries(instruments).map((entry) => (
            <>
              <input
                type="radio"
                id="instrument"
                key={entry[1]}
                value={entry[1]}
              />
              <label
                key={`instrument-${entry[0]}`}
                htmlFor={entry[1]}
                className="px-2"
              >
                {entry[1]}
              </label>
              <br />
            </>
          ))}
        </div>
      </fieldset>
      <fieldset>
        <legend className="text-xl">Instructors</legend>
        <div className="max-h-36 max-w-fit overflow-y-scroll">
          {Object.entries(instructors).map((entry) => (
            <>
              <input
                type="checkbox"
                name="instructor"
                id="instructor"
                key={entry[1].instructor}
                value={entry[1].instructor}
                defaultChecked={
                  instructorsArray.includes(entry[0]) ? true : false
                }
              />
              <label
                key={`instrument-${entry[0]}`}
                htmlFor={entry[1].instructor}
                className="px-2"
              >
                {entry[1].instructor}
              </label>
              <br />
            </>
          ))}
        </div>
      </fieldset>
      <input
        type="submit"
        value="Submit"
        className="rounded bg-green-800 hover:bg-green-700 text-zinc-200 hover:text-zinc-100 p-2 my-3"
      />
    </form>
  );
};

export default CourseForm;
