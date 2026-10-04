const {
    calculateCartTotal,
    calculateItemTotal,
    calculateDiscount,
    calculateGST
} = require('../cart');

describe("MS Mobiles Cart", function () {

    it("should calculate one mobile item total", function () {
        expect(calculateItemTotal(50000, 2)).toBe(100000);
    });

    it("should calculate total for multiple mobiles", function () {
        const items = [
            { price: 50000, quantity: 1 },
            { price: 30000, quantity: 2 }
        ];

        expect(calculateCartTotal(items)).toBe(110000);
    });

    it("should calculate discount", function () {
        expect(calculateDiscount(50000, 10)).toBe(45000);
    });

    it("should calculate GST", function () {
        expect(calculateGST(50000, 18)).toBe(59000);
    });

});