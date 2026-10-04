const { isValidProduct } = require('../product');

describe("MS Mobiles Product", function () {

    it("should accept a valid mobile product", function () {
        const product = {
            name: "Samsung Galaxy S25",
            price: 75000,
            quantity: 10
        };

        expect(isValidProduct(product)).toBeTruthy();
    });

    it("should reject a product with zero price", function () {
        const product = {
            name: "iPhone",
            price: 0,
            quantity: 5
        };

        expect(isValidProduct(product)).toBeFalsy();
    });

    it("should reject a product with negative price", function () {
        const product = {
            name: "OnePlus",
            price: -5000,
            quantity: 5
        };

        expect(isValidProduct(product)).toBeFalsy();
    });

});