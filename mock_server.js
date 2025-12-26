const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT || 5173;
const INDEX_PATH = path.join(__dirname, "index.html");

const mockResponse = {
  proposals: [
    {
      title: "Cozy Alpine Reset",
      description: "A calm, scenic week with light walks, warm cafes, and charming villages.",
      highlights: [
        "4–5 nights in a walkable alpine town",
        "Easy day trips with scenic rail views",
        "One special dinner with local flavors"
      ]
    },
    {
      title: "Seaside Wellness Escape",
      description: "Gentle ocean breezes, slow mornings, and relaxed coastal exploration.",
      highlights: [
        "Beachfront hotel with spa access",
        "Sunset strolls and markets",
        "Short sightseeing loop with flexible pacing"
      ]
    },
    {
      title: "City + Countryside Balance",
      description: "A cultural city base paired with a restful countryside retreat.",
      highlights: [
        "2 nights in the city for museums and food",
        "3–4 nights in a quiet village",
        "Private transfer or scenic train between"
      ]
    }
  ]
};

const server = http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/") {
    fs.readFile(INDEX_PATH, (err, data) => {
      if (err) {
        res.writeHead(500, { "Content-Type": "text/plain" });
        res.end("Failed to load index.html");
        return;
      }
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(data);
    });
    return;
  }

  if (req.method === "POST" && req.url === "/api/travel-proposals") {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk;
    });
    req.on("end", () => {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(mockResponse));
    });
    return;
  }

  res.writeHead(404, { "Content-Type": "text/plain" });
  res.end("Not found");
});

server.listen(PORT, () => {
  console.log(`Mock server running at http://localhost:${PORT}`);
});
