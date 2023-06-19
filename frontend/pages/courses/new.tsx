import { useUser, withPageAuthRequired } from "@auth0/nextjs-auth0";
import Layout from "../../components/layout";
import InstructorForm from "../../components/instructorForm";
import {
  CoursesQuery,
  IndexedStringList,
  InstructorsQuery,
  InstrumentsQuery,
} from "../../interfaces";
import { InferGetServerSidePropsType } from "next";
import CourseForm from "../../components/courseForm";

const dbURL = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function getServerSideProps() {
  const instrumentsRes = await fetch(`${dbURL}/instruments?per_page=1000`);
  const instrumentsData: InstrumentsQuery = await instrumentsRes.json();
  const instruments = instrumentsData.instruments;

  const instructorsRes = await fetch(`${dbURL}/instructors?per_page=1000`);
  const instructorsData: InstructorsQuery = await instructorsRes.json();
  const instructors = instructorsData.instructors;

  return {
    props: {
      instruments,
      instructors,
    },
  };
}

function Page({
  instruments,
  instructors,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  const { user, isLoading } = useUser();

  return (
    <Layout user={user} loading={isLoading}>
      <CourseForm
        method="POST"
        instruments={instruments}
        instructors={instructors}
      />
    </Layout>
  );
}

export default withPageAuthRequired(Page);
