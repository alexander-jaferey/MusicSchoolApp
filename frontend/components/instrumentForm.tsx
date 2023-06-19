import { useRouter } from "next/router";
import { IndexedInstructorList, Instrument } from "../interfaces";
import { alertService } from "../services";

type InstrumentFormProps = {
  method: string;
  instructors: IndexedInstructorList;
  values?: Instrument;
};

const InstrumentForm = ({
  method,
  instructors,
  values,
}: InstrumentFormProps) => {
  const router = useRouter();
  const handleSubmit = async (e) => {
    e.preventDefault();
    const instrument = e.target.instrument.value;
    const instructorOptions = e.target.instructor;
    let selectedInstructors = [];

    for (let i = 0; i < instructorOptions.length; i++) {
      if (instructorOptions[i].checked) {
        selectedInstructors.push(instructorOptions[i].value);
      }
    }

    const data = {
      instrument: instrument,
      instructors: selectedInstructors,
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
        ? `entity=instruments&id=${values.instrument_id}`
        : "entity=instruments";

    const response = await fetch(`/api/submit?${queryParams}`, request);
    const result = await response.json();
    console.log(result);

    const action = method === "PATCH" ? "update" : "add";

    if (result.error) {
      const error = result.error;
      const errorMessage = result.message;

      alertService.error(
        `Could not ${action} instrument (error ${error}: ${errorMessage})`,
        { id: "main" }
      );
    } else {
      alertService.success(`Instrument ${action}ed`);
      setTimeout(function () {
        router.push("/");
      }, 1000);
    }
  };

  const instructorsArray = values ? Object.keys(values.instructors) : [];

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="instrument" className="text-xl">
        Instrument
      </label>
      {values ? <div>Current: {values.instrument}</div> : <></>}
      <br />
      <input type="text" name="instrument" id="instrument" className="mb-3" />
      <fieldset>
        <legend className="text-xl">Instructors</legend>
        <div className="max-h-36 max-w-fit overflow-y-scroll">
          {Object.entries(instructors).map((entry) => (
            <>
              <input
                type="checkbox"
                name="instructor"
                id="instructor"
                key={`${entry[0]}-checkbox`}
                value={entry[1].instructor}
                defaultChecked={
                  instructorsArray.includes(entry[0]) ? true : false
                }
              />
              <label
                key={`${entry[0]}-label`}
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

export default InstrumentForm;
