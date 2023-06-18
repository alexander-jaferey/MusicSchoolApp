import { getAccessToken, withPageAuthRequired } from "@auth0/nextjs-auth0";
import { useEffect, useState } from "react";
import Layout from "../components/layout";
import { User } from "../interfaces";
import { stringify } from "querystring";

type ProfileCardProps = {
  user: User;
};

const ProfileCard = ({ user }: ProfileCardProps) => {
  const [token, setToken] = useState(null);

  useEffect(() => {
    (async () => {
      const res = await fetch("api/get-token");

      const token = await res.json();

      setToken(token);
    })();
  }, []);

  return (
    <>
      <h1>Profile</h1>

      <div>
        <h3>Profile (client rendered)</h3>
        <img src={user.picture} alt="user picture" />
        <p>nickname: {user.nickname}</p>
        <p>name: {user.name}</p>
        <div>{stringify(token)}</div>
      </div>
    </>
  );
};

const Profile = ({ user, isLoading }) => {
  return (
    <Layout user={user} loading={isLoading}>
      {isLoading ? <>Loading...</> : <ProfileCard user={user} />}
    </Layout>
  );
};

// Protected route, checking user authentication client-side.(CSR)
export default withPageAuthRequired(Profile);
