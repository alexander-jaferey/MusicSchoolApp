import { useRouter } from "next/router";
import { Deleted } from "../interfaces";
import { alertService } from "../services";

type DeleteProps = {
  id: number;
  entity: string;
  className?: string;
};

const DeleteButton = ({ id, entity, className }: DeleteProps) => {
  const router = useRouter();
  async function handleDelete() {
    if (confirm("Are you sure you want to delete this instrument?")) {
      const response = await fetch(`/api/delete?id=${id}&entity=${entity}`);
      const json: Deleted = await response.json();
      console.log(json);

      if (json.error) {
        const error = json.error;
        const errorMessage = json.message;

        alertService.error(
          `Could not delete instrument (error ${error}: ${errorMessage})`,
          { id: "main" }
        );
      }

      alertService.success("Instrument deleted", {
        id: "main",
        keepAfterRouteChange: true,
      });
      setTimeout(function () {
        router.push("/");
      }, 1000);
    }
  }

  return (
    <button
      className={`${className} rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-200 hover:text-zinc-100 p-2`}
      onClick={handleDelete}
    >
      Delete
    </button>
  );
};

export default DeleteButton;
