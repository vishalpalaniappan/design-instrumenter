import { spawn } from "node:child_process";

/**
 * Gets the mapping for the given file by running instrumenter in stream mode.
 * @param {String} file Path of the python script to map.
 * @param {Array} args The arguments to pass to the instrumenter.
 * @returns {Promise<String>} A promise that resolves with the output of the instrumenter.
 */
function getMapping(file, args = []) {
    return new Promise((resolve, reject) => {
        const process = spawn("python3", ["instrumenter.py", "parser_stream", ...args]);

        let stdout = "";
        let stderr = "";

        process.stdout.on("data", (data) => {
            stdout += data.toString();
        });

        process.stderr.on("data", (data) => {
            stderr += data.toString();
        });

        process.on("close", async (code) => {
            if (code !== 0) {
                reject(new Error(stderr || `Process exited with code ${code}`));
            } else {
                const outputData = stdout.trim();
                resolve(outputData);
            }
        });

        process.stdin.write(file);
        process.stdin.end();
    });
}

export default getMapping;