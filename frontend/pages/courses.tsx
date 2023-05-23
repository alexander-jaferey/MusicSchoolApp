import Layout from '../components/layout'
import { InferGetServerSidePropsType } from 'next';
import Link from 'next/link';
import { IndexedCourseList, IndexedStringList } from '../interfaces';

const dbURL = process.env.BACKEND_URL;

type Data = {
  courses: IndexedCourseList
  success: boolean
  total_instruments: number
};


export const getServerSideProps = async () => {
    const res = await fetch(dbURL + "/courses")
    const data: Data = await res.json()
   
    return {
      props: {
        data,
      },
    }
  }

  function Page({ data }: InferGetServerSidePropsType<typeof getServerSideProps>) {

    return <Layout>
        <div className="pb-4 border-b-2">
            <h1 className="text-3xl">Courses</h1>
        </div>
        <div>
            <ul>
                {Object.entries(data.courses).map((entry: [string, IndexedStringList]) => (
                    <li key={entry[0]} className="p-2">
                        <div className="text-lg font-bold">{entry[0]}:</div>
                        <ul>
                            {Object.entries(entry[1]).map((course: [string, string]) => (
                                <li key={course[0]} className="px-2"><Link className="text-green-800 hover:text-green-700"href={"/courses/" + course[0]}>{course[1]}</Link></li>
                            ))}
                        </ul>
                    </li>
               ))}
               {}
            </ul>
        </div>
    </Layout>
  }

export default Page;
