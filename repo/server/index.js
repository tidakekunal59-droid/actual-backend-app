const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const driverRoutes = require('./routes/drivers');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/drivers', driverRoutes);

module.exports = app;
