const express = require('express');
const router = express.Router();
const driverController = require('../controllers/driverController');

// Mock Auth
const authMiddleware = (req, res, next) => next();

router.post('/assign', authMiddleware, driverController.assignVehicle);

module.exports = router;
