import { NextApiRequest, NextApiResponse } from "next";

export let newstateSSEClient: NextApiResponse | null = null;

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    console.log('newstate_sse handler');
    // if (newstateSSEClient != null) {
    //     console.log('newstate_sse handler GG');
    //     res.status(403).send('Maximum number of SSE client already connected for /newstate');
    //     return;
    // }
    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Encoding': 'none',
        'Access-Control-Allow-Origin': '*'
    });
    res.on('close', () => {
        console.log('newstate_sse handler close');
    });
    res.on('open', () => {
        console.log('newstate_sse handler open');
    })
    res.on('message', () => {
        console.log('newstate_sse handler message');
    })
    newstateSSEClient = res;
    // newstateSSEClient = res;
    // console.log(newstateSSEClient == null)
    // newstateSSEClient?.write(event);
    res.status(200).write('success');
    // res.status(200).send('success');
}
