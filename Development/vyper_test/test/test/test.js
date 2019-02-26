const test = artifacts.require("test");
const assert = require("chai").assert;
const truffleAssert = require('truffle-assertions');

contract("test", (accounts) => {
    let test1;
    const fundingAccount = accounts[0];

    beforeEach(async () => {
        test1 = await test.new({from: fundingAccount});
    });
    
    it("should receive event", async() => {
        let tx = await test1.test();
        truffleAssert.eventEmitted(tx, 'Creation', (ev) => {
            return ev._test_a == 10000;
        });
    });
});