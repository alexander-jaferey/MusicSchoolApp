import { useRouter } from "next/router";
import { IndexedCourseList, IndexedStringList, Weekdays } from "../interfaces";
import { Instructor } from "../interfaces";
import { alertService } from "../services";

type InstructorFormProps = {
  method: string;
  instruments: IndexedStringList;
  courses: IndexedCourseList;
  values?: Instructor;
};

const InstructorForm = ({
  method,
  instruments,
  courses,
  values,
}: InstructorFormProps) => {
  const router = useRouter();
  const handleSubmit = async (e) => {
    e.preventDefault();
    const firstName = e.target.first_name.value;
    const lastName = e.target.last_name.value;
    const workdayOptions = e.target.weekday;
    const instrumentOptions = e.target.instrument;
    const courseOptions = e.target.course;

    let selectedWorkdays = [];
    let selectedInstruments = [];
    let selectedCourses = [];

    for (let i = 0; i < workdayOptions.length; i++) {
      if (workdayOptions[i].checked) {
        selectedWorkdays.push(workdayOptions[i].value);
      }
    }

    for (let i = 0; i < instrumentOptions.length; i++) {
      if (instrumentOptions[i].checked) {
        selectedInstruments.push(instrumentOptions[i].value);
      }
    }

    for (let i = 0; i < courseOptions.length; i++) {
      if (courseOptions[i].checked) {
        selectedCourses.push(courseOptions[i].value);
      }
    }

    const data = {
      first_name: firstName,
      last_name: lastName,
      workdays: selectedWorkdays,
      instruments: selectedInstruments,
      courses: selectedCourses,
    };
    const json = JSON.stringify(data);

    const request = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: json,
    };

    const queryParams =
      method === "PATCH"
        ? `entity=instructors&id=${values.instructor_id}`
        : "entity=instructors";

    const response = await fetch(`/api/submit?${queryParams}`, request);
    const result = await response.json();
    console.log(result);

    const action = method === "PATCH" ? "update" : "add";

    if (result.error) {
      const error = result.error;
      const errorMessage = result.message;

      alertService.error(
        `Could not ${action} instructor (error ${error}: ${errorMessage})`,
        { id: "main" }
      );
    } else {
      alertService.success(`Instructor ${action}ed`);
      setTimeout(function () {
        router.push("/");
      }, 1000);
    }
  };

  const instrumentsArray = values ? Object.keys(values.instruments) : [];
  const coursesArray = values ? Object.keys(values.courses_taught) : [];
  const workdaysArray = values ? values.workdays : [];

  return (
    <form onSubmit={handleSubmit}>
      <fieldset>
        <legend className="text-xl">Name</legend>
        {values ? <div>Current: {values.name}</div> : <></>}
        <label htmlFor="first_name">First Name</label>
        <br />
        <input type="text" name="first_name" id="first_name" className="mb-3" />
        <br />
        <label htmlFor="last_name">Last Name</label>
        <br />
        <input type="text" name="last_name" id="last_name" className="mb-3" />
        <br />
      </fieldset>
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
                defaultChecked={workdaysArray.includes(weekday) ? true : false}
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
      <div className="grid grid-cols-2">
        <div className="col-span-1">
          <fieldset>
            <legend className="text-xl">Instruments</legend>
            <div className="max-h-36 max-w-fit overflow-y-scroll">
              {Object.entries(instruments).map((entry) => (
                <>
                  <input
                    type="checkbox"
                    name="instrument"
                    id="instrument"
                    key={entry[1]}
                    value={entry[1]}
                    defaultChecked={
                      instrumentsArray.includes(entry[0]) ? true : false
                    }
                  />
                  <label key={entry[0]} htmlFor={entry[1]} className="px-2">
                    {entry[1]}
                  </label>
                  <br />
                </>
              ))}
            </div>
          </fieldset>
        </div>
        <div className="col-span-1">
          <fieldset>
            <legend className="text-xl">Courses</legend>
            <div className="max-h-36 max-w-fit overflow-y-scroll">
              {Object.entries(courses).map((instrument) => (
                <>
                  <div key={instrument[0]} className="pb-1">
                    {instrument[0]}
                  </div>
                  {Object.entries(instrument[1]).map((entry) => (
                    <>
                      <input
                        type="checkbox"
                        name="course"
                        id="course"
                        key={entry[1]}
                        value={entry[1]}
                        defaultChecked={
                          coursesArray.includes(entry[0]) ? true : false
                        }
                      />
                      <label key={entry[0]} htmlFor={entry[1]} className="px-2">
                        {entry[1]}
                      </label>
                      <br />
                    </>
                  ))}
                </>
              ))}
            </div>
          </fieldset>
        </div>
      </div>
      <input
        type="submit"
        value="Submit"
        className="rounded bg-green-800 hover:bg-green-700 text-zinc-200 hover:text-zinc-100 p-2 my-3"
      />
    </form>
  );
};

export default InstructorForm;
