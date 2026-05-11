import path from 'path';
import instrumentingRunner from './instrumentingRunner.js';
import {DALEngine} from "dal-engine-core-js-lib-dev";
import { resolveDesignPath } from "./validateDesignName.js";
import fs from 'fs/promises';
import unzipper from "unzipper";

const testStreamMode = async (designName) => {    
    const resolvedPath = resolveDesignPath(designName);
    const data = await fs.readFile(resolvedPath);
    const engine = new DALEngine({
        name: designName,
        description: "Default engine",
    });
    engine.deserialize(data);

    const instrumentationPkg = engine.implementation.exportForInstrumentation();

    try {
        const zipBuffer = await instrumentingRunner(instrumentationPkg);
        console.log("Instrumenter output:", zipBuffer);
        const directory = await unzipper.Open.buffer(zipBuffer);
        await directory.extract({ path: "./" });
    } catch (err) {
        console.error("Error during instrumenter execution:");
        console.error(err);
        process.exit(1);
    }
}

testStreamMode("lib_man_no_invariant.dal").catch((err) => {
    console.error("Error during test execution:", err);
    process.exit(1);
});