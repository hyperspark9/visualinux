// const MAX_SSE_CLIENTS = 2;
// export let newstateSSEClient: Response | null = null;

// export async function GET(request: Request) {
//     console.log('newstate_sse GET', request);
//     if (newstateSSEClient == null) {
//         newstateSSEClient = new Response('', {
//             status: 200,
//             headers: {
//                 'Content-Type': 'text/event-stream',
//                 'Cache-Control': 'no-cache',
//                 'Connection': 'keep-alive',
//                 'Access-Control-Allow-Origin': '*'
//             }
//         });
//     } else {
//         return new Response('Maximum number of SSE client already connected for /newstate', {
//             status: 403
//         });
//     }
//     return newstateSSEClient;
// }
