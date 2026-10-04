const { add, subtract } = require('../calculator');

describe("Calculator", function () {

    it("should add two numbers", function () {
        expect(add(2, 3)).toBe(5);
    });

    it("should subtract two numbers", function () {
        expect(subtract(5, 2)).toBe(3);
    });

});