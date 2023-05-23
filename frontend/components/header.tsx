import Link from 'next/link'

type HeaderProps = {
  user?: any
  loading: boolean
}

const Header = ({ user, loading }: HeaderProps) => (
  <header className="bg-zinc-800 text-zinc-200 py-4 px-6 justify-between grid grid-cols-5 font-global">
    <div className="container contents max-w-xl">
      <div className="col-span-1 ml-4">
      </div>
      <div className="flex col-span-3" >
        <Link href="/" className="text-lg font-semibold px-9">MusicSchoolApp</Link>
        <Link className="px-3" href="/instruments">instruments</Link>
        <Link className="px-3" href="/instructors">instructors</Link>
        <Link className="px-3" href="/courses">courses</Link>
      </div>
      <div className="justify-self-end flex mr-4">
        {!loading &&
          (user ? (
            <>
              <Link className="px-3" href="/profile">profile</Link>
              <Link className="px-3" href="/api/auth/logout">logout</Link>
            </>
          ) : (
            <>
              <Link className="px-3" href="/api/auth/login">login</Link>
            </>
          )
          )}
      </div>
    </div>
  </header>
)

export default Header
