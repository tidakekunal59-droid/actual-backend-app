const request = require('supertest');
const lockManager = require('../utils/lockManager');

// Mock external dependencies before requiring app
jest.mock('../models/Vehicle', () => ({
  findById: jest.fn()
}));
jest.mock('../models/Driver', () => ({
  findById: jest.fn(),
  findOne: jest.fn()
}));
jest.mock('../utils/lockManager', () => ({
  acquireLock: jest.fn(),
  releaseLock: jest.fn()
}));

// We need to delay requiring the app until mocks are set
const app = require('../index');
const Vehicle = require('../models/Vehicle');
const Driver = require('../models/Driver');

describe('Task 1: Concurrent Vehicle Assignment (Mocked)', () => {
  let token = 'mock-token';

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('Should allow assignment when lock is acquired', async () => {
    lockManager.acquireLock.mockResolvedValue(true);
    Driver.findById.mockResolvedValue({
      _id: 'd1',
      assignedVehicle: null,
      save: jest.fn().mockResolvedValue(true)
    });
    Vehicle.findById.mockResolvedValue({ _id: 'v1', status: 'active' });
    Driver.findOne.mockResolvedValue(null);

    const res = await request(app)
      .post('/api/drivers/assign')
      .set('Authorization', token)
      .send({ driverId: 'd1', vehicleId: 'v1' });

    expect(res.status).toBe(200);
    expect(lockManager.acquireLock).toHaveBeenCalled();
  });

  test('Should fail if lock cannot be acquired', async () => {
    lockManager.acquireLock.mockResolvedValue(false);

    const res = await request(app)
      .post('/api/drivers/assign')
      .set('Authorization', token)
      .send({ driverId: 'd2', vehicleId: 'v1' });

    expect(res.status).toBe(409);
  });
});
