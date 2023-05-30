import {
  getAccessToken,
  useUser,
  withPageAuthRequired,
} from "@auth0/nextjs-auth0";
import Layout from "../../components/layout";
import { DecodedJwt, Instrument } from "../../interfaces";
import React from "react";
import { InferGetServerSidePropsType } from "next";
import jwt_decode from "jwt-decode";
import Error from "next/error";
import Link from "next/link";

const dbURL = `${process.env.BACKEND_URL}/instruments/`;

export async function getServerSideProps(context: {
  params: { id: Number };
  req;
  res;
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

  const response = await fetch(`${dbURL}${id}`, {
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

  return {
    props: {
      data,
      permissions,
    },
  };
}

function Page({
  data,
  error,
  errorMessage,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  const { user, isLoading } = useUser();

  if (error) {
    return (
      <Layout>
        <Error statusCode={error} title={errorMessage} />
      </Layout>
    );
  }
  return (
    <Layout>
      <div className="pb-4 border-b-2">
        <h1 className="text-3xl">{data.instrument}</h1>
      </div>
      <div className="grid grid-cols-2">
        <div className="col-span-1 py-4">
          <h2 className="text-xl font-bold">Courses</h2>
          <ul className="py-2">
            {Object.entries(data.courses).map((entry: [string, string]) => (
              <li key={entry[0]} className="py-1">
                <Link
                  className="text-green-800 hover:text-green-700"
                  href={`/courses/${entry[0]}`}
                >
                  {entry[1]}
                </Link>
              </li>
            ))}
          </ul>
        </div>
        <div className="col-span-1 py-4">
          <h2 className="text-xl font-bold">Instructors</h2>
          <ul className="py-2">
            {Object.entries(data.instructors).map((entry: [string, string]) => (
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
      </div>
    </Layout>
  );
}

export default withPageAuthRequired(Page);
