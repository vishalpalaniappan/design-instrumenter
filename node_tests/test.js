import getMapping from './getMapping.js';
import fs from 'fs/promises';

const testStreamMode = async () => {
    const file = await fs.readFile("./sample/TransactionDB.py", 'utf-8');
    getMapping(file).then((mapping) => {
        console.log("Mapping output:", mapping);
    }).catch((err) => {
        console.error("Error during getMapping execution:", err);
        process.exit(1);
    });
}

testStreamMode().catch((err) => {
    console.error("Error during test execution:", err);
    process.exit(1);
});
