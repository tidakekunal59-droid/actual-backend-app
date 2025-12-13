const Driver = require('../models/Driver');
const Vehicle = require('../models/Vehicle');

exports.assignVehicle = async (req, res, next) => {
  try {
    const { driverId, vehicleId } = req.body;

    const driver = await Driver.findById(driverId);
    if (!driver) return res.status(404).json({ message: 'Driver not found' });

    const vehicle = await Vehicle.findById(vehicleId);
    if (!vehicle) return res.status(404).json({ message: 'Vehicle not found' });

    if (vehicle.status !== 'active') {
      return res.status(400).json({ message: 'Vehicle is not active' });
    }

    // Check if vehicle is already assigned
    const existingAssignment = await Driver.findOne({ assignedVehicle: vehicleId });
    if (existingAssignment && existingAssignment.id !== driverId) {
      return res.status(409).json({ message: 'Vehicle already assigned to another driver' });
    }

    driver.assignedVehicle = vehicleId;
    await driver.save();

    res.json(driver);
  } catch (err) {
    next(err);
  }
};
