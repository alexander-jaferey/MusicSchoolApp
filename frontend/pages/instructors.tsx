import Layout from "../components/layout";
import { InferGetServerSidePropsType } from "next";
import Link from "next/link";
import { IndexedInstructorList, InstructorInfo } from "../interfaces";
import { useUser } from "@auth0/nextjs-auth0";
import Pagination from "../components/pagination";

const dbURL = `${process.env.NEXT_PUBLIC_BACKEND_URL}/instructors`;

type Data = {
  instructors: IndexedInstructorList;
  success: boolean;
  total_instructors: number;
  current_page: number;
  total_pages: number;
};

export async function getServerSideProps(context: { query: { page: number } }) {
  const page = context.query.page || 1;

  const res = await fetch(`${dbURL}?page=${page}`);
  const data: Data = await res.json();

  return {
    props: {
      data,
    },
  };
}

function Page({
  data,
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
        <h1 className="text-3xl">Instructors</h1>
      </div>
      <div>
        {isLoading && <div>Loading...</div>}
        {!isLoading && (
          <ul>
            {Object.entries(data.instructors).map(
              (entry: [string, InstructorInfo]) => (
                <li key={entry[0]} className="p-2">
                  <Link
                    className="text-lg font-bold text-green-800 hover:text-green-700"
                    href={"/instructors/" + entry[0]}
                  >
                    {entry[1].instructor}
                  </Link>
                  <br />
                  <ul>
                    {entry[1].instruments.map((instrument: string) => (
                      <li key={instrument} className="px-2 text-sm">
                        {instrument}
                      </li>
                    ))}
                  </ul>
                </li>
              )
            )}
            {}
          </ul>
        )}
      </div>
      <br />
      <Pagination
        target="instructors"
        currentPage={data.current_page}
        totalPages={data.total_pages}
        pages={pages}
      />
    </Layout>
  );
}

export default Page;
