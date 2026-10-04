function calculateTotal(price, quantity) {
    return price * quantity;
}

function calculateDiscount(price, discount) {
    return price - (price * discount / 100);
}

module.exports = {
    calculateTotal,
    calculateDiscount
};