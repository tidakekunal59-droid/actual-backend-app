const Driver = require('../models/Driver');
const Vehicle = require('../models/Vehicle');
const lockManager = require('../utils/lockManager');

exports.assignVehicle = async (req, res, next) => {
  const { driverId, vehicleId } = req.body;
  const lockResource = `vehicle:${vehicleId}`;

  try {
    const locked = await lockManager.acquireLock(lockResource, driverId);
    if (!locked) {
      return res.status(409).json({ message: 'Vehicle is currently being modified by another request. Please try again.' });
    }

    const driver = await Driver.findById(driverId);
    if (!driver) {
      await lockManager.releaseLock(lockResource, driverId);
      return res.status(404).json({ message: 'Driver not found' });
    }

    const vehicle = await Vehicle.findById(vehicleId);
    if (!vehicle) {
      await lockManager.releaseLock(lockResource, driverId);
      return res.status(404).json({ message: 'Vehicle not found' });
    }

    if (vehicle.status !== 'active') {
      await lockManager.releaseLock(lockResource, driverId);
      return res.status(400).json({ message: 'Vehicle is not active' });
    }

    const existingAssignment = await Driver.findOne({ assignedVehicle: vehicleId });
    if (existingAssignment && existingAssignment.id !== driverId) {
      await lockManager.releaseLock(lockResource, driverId);
      return res.status(409).json({ message: 'Vehicle already assigned to another driver' });
    }

    driver.assignedVehicle = vehicleId;
    await driver.save();

    await lockManager.releaseLock(lockResource, driverId);

    res.json(driver);
  } catch (err) {
    await lockManager.releaseLock(lockResource, driverId).catch(() => {});
    next(err);
  }
};
