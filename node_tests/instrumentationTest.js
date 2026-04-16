import instrumentingRunner from './instrumentingRunner.js';
import fs from 'fs/promises';
import unzipper from "unzipper";

const testStreamMode = async () => {
    const file = await fs.readFile("./sample/execution_trace_walker.dal.json", 'utf-8');
    instrumentingRunner(file).then(async(zipBuffer) => {
        console.log("Instrumenter output:", zipBuffer);
        const directory = await unzipper.Open.buffer(zipBuffer);
        await directory.extract({ path: "./" });
    }).catch((err) => {
        console.error("Error during instrumenter execution:");
        console.error(err);
        process.exit(1);
    });
}

testStreamMode().catch((err) => {
    console.error("Error during test execution:", err);
    process.exit(1);
});