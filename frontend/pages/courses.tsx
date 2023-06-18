import Layout from "../components/layout";
import { InferGetServerSidePropsType, NextApiRequest, NextApiResponse } from "next";
import Link from "next/link";
import { CoursesQuery, DecodedJwt, IndexedCourseList, IndexedStringList } from "../interfaces";
import { getAccessToken, useUser } from "@auth0/nextjs-auth0";
import Pagination from "../components/pagination";
import jwt_decode from 'jwt-decode';

const dbURL = `${process.env.NEXT_PUBLIC_BACKEND_URL}/courses`;

export async function getServerSideProps(context: { query: { page: number }; req: NextApiRequest; res: NextApiResponse }) {
  const page = context.query.page || 1;
  const req = context.req;
  const res = context.res;

  const response = await fetch(`${dbURL}?page=${page}`);
  const data: CoursesQuery = await response.json();

  if (req.cookies.appSession) {
    const accessToken = (await getAccessToken(req, res)).accessToken
    const token: DecodedJwt = jwt_decode(accessToken)
    const permissions = token.permissions
    return {
      props: {
        data,
        permissions
      },
    };
  }
  else {
    const permissions = []
    return {
      props: {
        data,
        permissions
      },
    };
  }
}

function Page({
  data,
  permissions
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  const { user, isLoading } = useUser();

  let pages: number[] = [];
  let i: number = 1;
  while (i <= data.total_pages) {
    pages.push(i);
    i++;
  }

  return (
    <Layout user={user} loading={isLoading}>
      <div className="pb-4 border-b-2">
      {permissions.includes("post:courses") ? 
          <Link href="/courses/new" className="rounded mr-2 bg-green-800 hover:bg-green-700 text-zinc-200 hover:text-zinc-100 hover:no-underline p-2 float-right">New Course</Link> : <></>
        }
        <h1 className="text-3xl">Courses</h1>
      </div>
      <div>
        <ul>
          {Object.entries(data.courses).map(
            (entry: [string, IndexedStringList]) => (
              <li key={entry[0]} className="p-2">
                <div className="text-lg font-bold">{entry[0]}:</div>
                <ul>
                  {Object.entries(entry[1]).map((course: [string, string]) => (
                    <li key={course[0]} className="px-2">
                      <Link
                        className="text-green-800 hover:text-green-700"
                        href={"/courses/" + course[0]}
                      >
                        {course[1]}
                      </Link>
                    </li>
                  ))}
                </ul>
              </li>
            )
          )}
          {}
        </ul>
      </div>
      <br />
      <Pagination
        target="courses"
        currentPage={data.current_page}
        totalPages={data.total_pages}
        pages={pages}
      />
    </Layout>
  );
}

export default Page;
