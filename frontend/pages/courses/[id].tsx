import {
  getAccessToken,
  useUser,
  withPageAuthRequired,
} from "@auth0/nextjs-auth0";
import Layout from "../../components/layout";
import { Course, DecodedJwt} from "../../interfaces";
import React from "react";
import { InferGetServerSidePropsType, NextApiRequest, NextApiResponse } from "next";
import jwt_decode from "jwt-decode";
import Error from "next/error";
import Link from "next/link";

const dbURL = `${process.env.NEXT_PUBLIC_BACKEND_URL}/courses/`;

export async function getServerSideProps(context: {
  params: { id: Number };
  req: NextApiRequest;
  res: NextApiResponse;
}) {
  const req = context.req;
  const res = context.res;
  const id = context.params.id;

  const accessToken = (await getAccessToken(req, res)).accessToken;
  const token: DecodedJwt = jwt_decode(accessToken);
  const permissions = token.permissions;

  const error = permissions.includes("get:courses") ? false : 403;

  if (error) {
    const errorMessage: string = "You don't have permission to view this page";
    return {
      props: {
        error,
        errorMessage,
      },
    };
  }

  const response = await fetch(`${dbURL}${id}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  const data: Course = await response.json();

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

  return {
    props: {
      data,
      permissions,
      token,
    },
  };
}

function Page({
  data,
  permissions,
  token,
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
    <Layout>
      <div className="grid grid-cols-2 pb-4 border-b-2">
        <div className="col-span-1">
          <h1 className="text-3xl">{data.course_title}</h1>
        </div>
        <div className="col-span-1 flex flex-row flex-auto pt-3 font-bold">
          <div className="px-1">Instrument: </div>
          <Link href={`/instruments/${data.instrument.id}`} className="text-green-800 hover:text-green-700">{data.instrument.name}</Link>
        </div>
      </div>
      <div className="grid grid-cols-2">
        <div className="col-span-1 py-4">
          <h2 className="text-xl font-bold">Instructors</h2>
          <ul className="py-2">
            {data.instructors[0] ? <div className="py-1">{data.instructors[0]}</div> :
            Object.entries(data.instructors).map((entry: [string, string]) => (
              <li key={entry[0]} className="py-1">
                <Link
                  className="text-green-800 hover:text-green-700"
                  href={`/instructors/${entry[0]}`}
                >
                  {entry[1]}
                </Link>
              </li>
            ))}
          </ul>
        </div>
        <div className="col-span-1 py-4">
          <h2 className="text-xl font-bold">Schedule</h2>
          <ul className="py-2">
            {data.schedule.map((day) => (
              <li key={day} className="py-1">{day}</li>
            ))}
          </ul>
        </div>
      </div>
    </Layout>
  );
}

export default withPageAuthRequired(Page);