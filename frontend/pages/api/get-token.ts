import { getAccessToken, withApiAuthRequired } from "@auth0/nextjs-auth0";

const token = withApiAuthRequired(async function getToken(req, res) {
  const accessToken = await getAccessToken(req, res);
  res.status(200).json(accessToken);
});

export default token;
