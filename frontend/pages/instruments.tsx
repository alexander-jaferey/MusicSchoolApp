import Layout from '../components/layout'
import { InferGetServerSidePropsType } from 'next';
import Link from 'next/link';
import { IndexedList } from '../interfaces';

const dbURL = process.env.BACKEND_URL;

type Data = {
  instruments: IndexedList
  success: boolean
  total_instruments: number
}


export const getServerSideProps = async () => {
    const res = await fetch(dbURL + "/instruments")
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
            <h1 className="text-3xl">Instruments</h1>
        </div>
        <div>
            <ul>
                {Object.entries(data.instruments).map((entry: [string, string]) => (
                    <li key={entry[0]} className="p-2"><Link className="text-lg font-bold text-green-800 hover:text-green-700" href={"/instruments/" + entry[0]}>{entry[1]}</Link></li>
               ))}
               {}
            </ul>
        </div>
    </Layout>
  }

export default Page;
