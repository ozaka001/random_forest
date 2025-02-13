const { spawn } = require("child_process");
const path = require("path");

exports.handler = async function (event, context) {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  try {
    const data = JSON.parse(event.body);

    // Call Python script with data
    const pythonProcess = spawn("python", [
      path.join(__dirname, "predict.py"),
      JSON.stringify(data.data),
    ]);

    return new Promise((resolve, reject) => {
      let result = "";

      pythonProcess.stdout.on("data", (data) => {
        result += data.toString();
      });

      pythonProcess.stderr.on("data", (data) => {
        console.error(`Error: ${data}`);
      });

      pythonProcess.on("close", (code) => {
        resolve({
          statusCode: 200,
          headers: {
            "Content-Type": "application/json",
          },
          body: result,
        });
      });
    });
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Failed to process request" }),
    };
  }
};
