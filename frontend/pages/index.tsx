import { useUser } from "@auth0/nextjs-auth0";
import Layout from "../components/layout";

const Home = () => {
  const { user, isLoading } = useUser();

  return (
    <Layout user={user} loading={isLoading}>
      {isLoading && <p>Loading login info...</p>}

      {!isLoading && (
        <>
          <h2 className="text-xl font-bold">Music School App</h2>
          <p>Application to retrieve and edit information on musical courses for various instruments and their instructors.</p>
          <br /><br />
        </>
      )}

      {!isLoading && !user && (
        <>
          <p>
            To test the login click in <i>Login</i>
          </p>
          <p>
            Once you have logged in you should be able to navigate between
            protected routes: client rendered, server rendered profile pages,
            and <i>Logout</i>
          </p>
        </>
      )}

      {user && (
        <>
          <h4>Rendered user info on the client</h4>
          <img src={user.picture} alt="user picture" />
          <p>nickname: {user.nickname}</p>
          <p>name: {user.name}</p>
        </>
      )}
    </Layout>
  );
};

// fast/cached SSR page
export default Home;
