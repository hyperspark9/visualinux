'use server'

import MainWrapper from "@app/main";

import { readLocal } from "@app/local";
import { preprocess } from "@app/visual/preprocess";
import { View } from "@app/visual/type";
const DumpPath = '/public/statedump/latest.json';

export default async function Page() {
    let initData: View = JSON.parse(await readLocal(DumpPath));
    preprocess(initData);
    return (
        <MainWrapper initData={initData}/>
    )
}
