import { spawn } from "node:child_process";

/**
 * Gets the mapping for the given python source by invoking the instrumenter in stream mode.
 * @param {String} source Python source code to be processed by the instrumenter.
 * @param {Array} args The arguments to pass to the instrumenter.
 * @returns {Promise<String>} A promise that resolves with the output of the instrumenter.
 */
function instrument(source, args = []) {
    return new Promise((resolve, reject) => {
        const process = spawn("python3", ["instrumenter.py", "instrumenter_stream", ...args]);
                let settled = false;

        const stdoutChunks = [];
        const stderr = "";


        process.stdout.on("data", (data) => {
            stdoutChunks.push(data);
        });

        process.stderr.on("data", (data) => {
            stderr += data.toString();
        });

        process.on("error", (err) => {
            if (settled) return;
            settled = true;
            reject(err);
        });

        process.on("close", async (code) => {
            if (settled) return;
            settled = true;
            if (code !== 0) {
                reject(new Error(stderr || `Process exited with code ${code}`));
            } else {
                resolve(Buffer.concat(stdoutChunks));
            }
        });

        if (typeof source !== "string") {
            reject(new Error("source must be a string"));
            return;
        }

        process.stdin.write(source);
        process.stdin.end();
    });
}

export default instrument;