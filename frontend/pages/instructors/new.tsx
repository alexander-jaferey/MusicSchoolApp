import { useUser, withPageAuthRequired } from "@auth0/nextjs-auth0";
import Layout from "../../components/layout";
import InstructorForm from "../../components/instructorForm";
import { CoursesQuery, IndexedStringList, InstrumentsQuery } from "../../interfaces";
import { InferGetServerSidePropsType } from "next";

const dbURL = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function getServerSideProps() {
  const instRes = await fetch(`${dbURL}/instruments?per_page=1000`);
  const instData : InstrumentsQuery = await instRes.json();
  const instruments = instData.instruments;

  const courseRes = await fetch (`${dbURL}/courses?per_page=1000`);
  const courseData: CoursesQuery = await courseRes.json();
  const courses = courseData.courses;

  return {
    props: {
      instruments,
      courses
    }
  }
}

function Page({
  instruments,
  courses
}: InferGetServerSidePropsType <typeof getServerSideProps>) {
  const { user, isLoading } = useUser();

  return (
    <Layout user={user} loading={isLoading}>
      <InstructorForm method="POST" instruments={instruments} courses={courses} />
    </Layout>
  )
}

export default withPageAuthRequired(Page)