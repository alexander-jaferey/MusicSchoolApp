import { getAccessToken, withApiAuthRequired } from "@auth0/nextjs-auth0";
import { NextApiRequest, NextApiResponse } from "next";
import { Deleted} from "../../interfaces";

const dbURL = `${process.env.NEXT_PUBLIC_BACKEND_URL}/`;

async function deleteEntity(req: NextApiRequest, res: NextApiResponse): Promise<void> {
    const id = req.query.id;
    const entity = req.query.entity;

    const accessToken = (await getAccessToken(req, res)).accessToken;

    const deleted = await fetch(`${dbURL}${entity}/${id}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });
    const response: Deleted = await deleted.json();

    if (response.error) {
        res.status(response.error).json(response)
    }

    res.status(200).json(response)
}

export default withApiAuthRequired(deleteEntity)