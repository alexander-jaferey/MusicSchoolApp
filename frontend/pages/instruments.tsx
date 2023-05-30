import Layout from "../components/layout";
import { InferGetServerSidePropsType } from "next";
import Link from "next/link";
import { IndexedStringList } from "../interfaces";
import { useUser } from "@auth0/nextjs-auth0";
import Pagination from "../components/pagination";

const dbURL = `${process.env.BACKEND_URL}/instruments`;

type Data = {
  instruments: IndexedStringList;
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
        <h1 className="text-3xl">Instruments</h1>
      </div>
      <div>
        {isLoading && <div>Loading...</div>}
        {!isLoading && (
          <ul>
            {Object.entries(data.instruments).map((entry: [string, string]) => (
              <li key={entry[0]} className="p-2">
                <Link
                  className="text-lg font-bold text-green-800 hover:text-green-700"
                  href={"/instruments/" + entry[0]}
                >
                  {entry[1]}
                </Link>
              </li>
            ))}
            {}
          </ul>
        )}
      </div>
      <br />
      <Pagination
        target="instruments"
        currentPage={data.current_page}
        totalPages={data.total_pages}
        pages={pages}
      />
    </Layout>
  );
}

export default Page;
