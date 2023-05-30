import Layout from "../components/layout";
import { InferGetServerSidePropsType } from "next";
import Link from "next/link";
import { IndexedCourseList, IndexedStringList } from "../interfaces";
import { useUser } from "@auth0/nextjs-auth0";
import Pagination from "../components/pagination";

const dbURL = `${process.env.BACKEND_URL}/courses`;

type Data = {
  courses: IndexedCourseList;
  success: boolean;
  total_instruments: number;
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
