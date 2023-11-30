// server.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

let isMuted = false;

app.get('/mute-status', (req, res) => {
    res.json({ isMuted });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
