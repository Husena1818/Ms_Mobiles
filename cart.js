function calculateCartTotal(items) {
    return items.reduce((total, item) => {
        return total + (item.price * item.quantity);
    }, 0);
}

function calculateItemTotal(price, quantity) {
    return price * quantity;
}

function calculateDiscount(total, discountPercent) {
    return total - (total * discountPercent / 100);
}

function calculateGST(total, gstPercent) {
    return total + (total * gstPercent / 100);
}

module.exports = {
    calculateCartTotal,
    calculateItemTotal,
    calculateDiscount,
    calculateGST
};