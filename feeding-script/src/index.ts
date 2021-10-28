import * as dotenv from "dotenv";
import { Application } from "./app";
dotenv.config();

const run = async () => {
    console.log('\n======================================================\n');
    new Application().run();
    console.log('\n======================================================\n');
}

run();