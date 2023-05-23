import Layout from '../components/layout'
import { InferGetServerSidePropsType } from 'next';
import Link from 'next/link';
import { IndexedObjectList, InstructorInfo } from '../interfaces';

const dbURL = process.env.BACKEND_URL;

type Data = {
  instructors: IndexedObjectList
  success: boolean
  total_instructors: number
};


export const getServerSideProps = async () => {
    const res = await fetch(dbURL + "/instructors")
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
            <h1 className="text-3xl">Instructors</h1>
        </div>
        <div>
            <ul>
                {Object.entries(data.instructors).map((entry: [string, InstructorInfo]) => (
                    <li key={entry[0]} className="p-2">
                        <Link className="text-lg font-bold text-green-800 hover:text-green-700" href={"/instructors/" + entry[0]}>{entry[1].instructor}</Link>
                        <br />
                        <div className="pl-1 pt-1">Instruments:</div>
                        <ul>
                            {entry[1].instruments.map((instrument: string) => (
                                <li key={instrument}className="px-2 text-sm">{instrument}</li>
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
