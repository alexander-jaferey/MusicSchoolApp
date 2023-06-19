import { getAccessToken, withApiAuthRequired } from "@auth0/nextjs-auth0";
import { NextApiRequest, NextApiResponse } from "next";

const dbURL = `${process.env.NEXT_PUBLIC_BACKEND_URL}/`;

async function submitRequest(req: NextApiRequest, res: NextApiResponse) {
  const entity = req.query.entity;
  const method = req.method;
  const requestURL =
    req.method === "PATCH"
      ? `${dbURL}${entity}/${req.query.id}`
      : `${dbURL}${entity}`;
  const accessToken = (await getAccessToken(req, res)).accessToken;

  const request = {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(req.body),
  };

  const submitted = await fetch(requestURL, request);

  const response = await submitted.json();
  if (response.error) {
    res.status(response.error).json(response);
  } else {
    res.status(200).json(response);
  }
}

export default withApiAuthRequired(submitRequest);
