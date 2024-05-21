import { NextApiRequest, NextApiResponse } from "next";
// import { newstateSSEClient } from "./newstate_sse";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const data = JSON.stringify(req.body);
    const event = `data: ${data}\n\n`;
    console.log('/newstate receive data: ', data);
    console.log('ssewrite', event);
    // console.log(newstateSSEClient == null)
    // newstateSSEClient?.write(event);
    res.status(200).send('success');
}
