import { useRouter } from "next/router";
import { IndexedInstructorList, Instrument } from "../interfaces";
import { alertService } from "../services";

type InstrumentFormProps = {
  method: string
  instructors: IndexedInstructorList 
  values?: Instrument
};

type InstrumentSubmission = {
  instrument: string
  instructors?: string[]
}

const InstrumentForm = ({ method, instructors, values } : InstrumentFormProps) => {
  const handleSubmit = async (e) => {
    e.preventDefault();
    const router = useRouter();
    const instrument = e.target.instrument.value;
    const instructorOptions = e.target.instructor;
    let selectedInstructors = [];
    
    for (let i = 0; i < instructorOptions.length; i++) {
      if (instructorOptions[i].checked) {
        selectedInstructors.push(instructorOptions[i].value);
      };
    };

    const data = {
      instrument: instrument,
      instructors: selectedInstructors
    };
    const json = JSON.stringify(data);

    const request = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: json,
    };

    const response = await fetch("/api/submit?entity=instruments", request);
    const result = await response.json();
    console.log(result)

    if (result.error) {
      const error = result.error;
      const errorMessage = result.message;

      alertService.error(`Could not ${method.toLowerCase} instrument (error ${error}: ${errorMessage})`, { id: "main" })
    }
    else {
      alertService.success(`Instrument ${method.toLowerCase}ed`)
      setTimeout(function() {
        router.push("/")
      }, 1000)
    }

  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="instrument" className="text-xl">Instrument</label><br />
      <input type="text" name="instrument" id="instrument" className="mb-3"/>
      <fieldset>
        <legend className="text-xl">Instructors</legend>
        <div className="max-h-36 max-w-fit overflow-y-scroll">
          {Object.entries(instructors).map(
            (entry => (
              <><input type="checkbox" name="instructor" id="instructor" value={entry[1].instructor} />
              <label htmlFor={entry[1].instructor} className="px-2">{entry[1].instructor}</label><br /></>
            ))
          )}
          </div>
      </fieldset>
      <input type="submit" value="Submit" className="rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-200 p-2 my-3"/>
    </form> 
  );
};

export default InstrumentForm;
