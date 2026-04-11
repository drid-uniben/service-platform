import app from "./app.js";

const port = Number(process.env.PORT ?? 4000);

app.listen(port, () => {
  // Keep startup output short and explicit for local development.
  console.log(`auth-service listening on http://localhost:${port}`);
});
