const express = require("express");
const { MongoClient } = require("mongodb");

const app = express();
const port = process.env.PORT || 3000;
const mongoUrl = process.env.MONGO_URL || "mongodb://mongo:27017/mydb";

let db;

app.get("/health", (_req, res) => {
  res.status(200).json({ status: "ok" });
});

app.get("/", async (_req, res) => {
  try {
    const collections = db ? await db.listCollections().toArray() : [];
    res.type("html").send(
      `<!doctype html><html><body>
        <h1>Node.js + MongoDB</h1>
        <p>Connected: ${db ? "yes" : "no"}</p>
        <p>Collections: ${collections.map((c) => c.name).join(", ") || "(none)"}</p>
      </body></html>`
    );
  } catch (err) {
    res.status(500).json({ error: String(err.message || err) });
  }
});

async function start() {
  const client = new MongoClient(mongoUrl);
  await client.connect();
  db = client.db();
  app.listen(port, () => {
    console.log(`Listening on ${port}`);
  });
}

start().catch((err) => {
  console.error(err);
  process.exit(1);
});
