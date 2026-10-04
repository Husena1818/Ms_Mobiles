const {
    calculateTotal,
    calculateDiscount
} = require('../mobile');

describe("MS Mobiles", function () {

    it("should calculate total mobile price", function () {
        expect(calculateTotal(50000, 2)).toBe(100000);
    });

    it("should calculate discount price", function () {
        expect(calculateDiscount(50000, 10)).toBe(45000);
    });

});