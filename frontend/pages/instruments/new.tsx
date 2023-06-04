import { useUser, withPageAuthRequired } from "@auth0/nextjs-auth0";
import Layout from "../../components/layout";
import InstrumentForm from "../../components/instrumentForm";
import { InstructorsQuery } from "../../interfaces";
import { InferGetServerSidePropsType } from "next";

const dbURL = process.env.NEXT_PUBLIC_BACKEND_URL

export async function getServerSideProps() {
  const res = await fetch(`${dbURL}/instructors?per_page=1000`);
  const data: InstructorsQuery = await res.json();
  const instructors = data.instructors

  return {
    props: {
      instructors,
    },
  };
}

function Page({
    instructors,
  }: InferGetServerSidePropsType<typeof getServerSideProps>
) {
  const { user, isLoading } = useUser();

  return (
    <Layout user={user} loading={isLoading}>
      <InstrumentForm method="POST" instructors={instructors}/>
    </Layout>
  );
}

export default withPageAuthRequired(Page);
