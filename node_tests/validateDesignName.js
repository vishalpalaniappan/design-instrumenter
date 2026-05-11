import path from "node:path";

const WORKSPACE = path.resolve(process.cwd(), "sample");
const VALID_NAME = /^[A-Za-z0-9_\-]+\.dal$/;

/**
 * Validates designName and returns the resolved, safe file path.
 * Throws if the name is missing, malformed, or escapes the workspace.
 */
export function resolveDesignPath(designName) {
    if (!designName) {
        throw new Error("Design name is required.");
    }

    if (!VALID_NAME.test(designName)) {
        throw new Error("Invalid design name. Only alphanumeric characters, underscores, hyphens and the .dal extension are allowed.");
    }

    if (path.basename(designName) !== designName || !designName.endsWith(".dal")) {
        throw new Error("Invalid design name.");
    }
    
    const filePath = path.resolve(WORKSPACE, designName);

    // This check might be redundant with the path.basename check, but it's an extra layer of security that I'll keep.
    if (!filePath.startsWith(WORKSPACE + path.sep)) {
        throw new Error("Invalid design name.");
    }
    return filePath;
}