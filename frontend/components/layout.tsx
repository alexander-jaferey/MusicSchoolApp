import Head from 'next/head'
import Header from './header'

type LayoutProps = {
  user?: any
  loading?: boolean
  children: React.ReactNode
}

const Layout = ({ user, loading = false, children }: LayoutProps) => {
  return (
    <>
      <Head>
        <title>{process.env.APP_NAME}</title>
      </Head>

      <Header user={user} loading={loading} />

      <main className="m-6 text-zinc-800 py-4 px-6 justify-between grid grid-cols-4 font-global">
        <div className="col-span-1"></div>
        <div className="max-w-4xl m-6 col-span-2">{children}</div>
        <div className="col-span-1"></div>
      </main>
    </>
  )
}

export default Layout
