function isValidProduct(product) {
    return (
        product.name &&
        product.price > 0 &&
        product.quantity >= 0
    );
}

module.exports = {
    isValidProduct
};