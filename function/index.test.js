
const mockSet = jest.fn();
const mockDoc = jest.fn(() => ({ set: mockSet }));
const mockCollection = jest.fn(() => ({ doc: mockDoc }));
const mockFirestore = jest.fn(() => ({ collection: mockCollection }));

const mockAdmin = {
  initializeApp: jest.fn(),
  firestore: mockFirestore
};

jest.mock('firebase-admin', () => mockAdmin);

const test = require('firebase-functions-test')();
const myFunctions = require('./index');

describe('onUserCreate', () => {
    it('should select random profile image', async () => {
        const wrapped = test.wrap(myFunctions.onUserCreate);
        // call multiple times
        const images = new Set();

        // We expect at least 2 distinct URLs if the function works as intended (randomly selecting from different images)
        for(let i=0; i<50; i++) {
             mockSet.mockClear();
             await wrapped({ uid: 'u'+i, email: 'e'+i });

             // Check what was passed to set
             // The first call to set should contain the userProfile
             const callArgs = mockSet.mock.calls[0][0];
             images.add(callArgs.userProfile.profileImage);
        }
        // console.log('Unique images found:', images.size);
        expect(images.size).toBeGreaterThan(1);
    });
});
