import * as dotenv from "dotenv";
import { Application } from "./app";

dotenv.config();
new Application().run();