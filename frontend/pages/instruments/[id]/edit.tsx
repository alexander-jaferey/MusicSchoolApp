import {
  getAccessToken,
  useUser,
  withPageAuthRequired,
} from "@auth0/nextjs-auth0";
import {
  InferGetServerSidePropsType,
  NextApiRequest,
  NextApiResponse,
} from "next";
import { DecodedJwt, InstructorsQuery, Instrument } from "../../../interfaces";
import jwt_decode from "jwt-decode";
import Error from "next/error";
import Layout from "../../../components/layout";
import InstrumentForm from "../../../components/instrumentForm";

const dbURL = process.env.NEXT_PUBLIC_BACKEND_URL;

export async function getServerSideProps(context: {
  params: { id: number };
  req: NextApiRequest;
  res: NextApiResponse;
}) {
  const req = context.req;
  const res = context.res;
  const id = context.params.id;

  const accessToken = (await getAccessToken(req, res)).accessToken;
  const token: DecodedJwt = jwt_decode(accessToken);
  const permissions = token.permissions;

  const error = permissions.includes("get:instruments") ? false : 403;

  if (error) {
    const errorMessage: string = "You don't have permission to view this page";
    return {
      props: {
        error,
        errorMessage,
      },
    };
  }

  const response = await fetch(`${dbURL}/instruments/${id}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  const data: Instrument = await response.json();

  if (data.success == false) {
    const error = data.error;
    const errorMessage = data.message;

    return {
      props: {
        error,
        errorMessage,
      },
    };
  }

  const instructorsRes = await fetch(`${dbURL}/instructors?per_page=1000`);
  const instructorsData: InstructorsQuery = await instructorsRes.json();
  const instructors = instructorsData.instructors;

  return {
    props: {
      data,
      instructors,
    },
  };
}

function Page({
  data,
  instructors,
  error,
  errorMessage,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  const { user, isLoading } = useUser();

  if (error) {
    return (
      <Layout user={user} loading={isLoading}>
        <Error statusCode={error} title={errorMessage} />
      </Layout>
    );
  }

  return (
    <Layout user={user} loading={isLoading}>
      <InstrumentForm method="PATCH" instructors={instructors} values={data} />
    </Layout>
  );
}

export default withPageAuthRequired(Page);
