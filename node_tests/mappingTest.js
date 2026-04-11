import stmtMappingRunner from './stmtMappingRunner.js';
import fs from 'fs/promises';

const testStreamMode = async () => {
    const file = await fs.readFile("./sample/TransactionDB.py", 'utf-8');
    stmtMappingRunner(file).then((mapping) => {
        console.log("Mapping output:", mapping);
    }).catch((err) => {
        console.error("Error during stmtMappingRunner execution:");
        console.error(err);
        process.exit(1);
    });
}

testStreamMode().catch((err) => {
    console.error("Error during test execution:", err);
    process.exit(1);
});
