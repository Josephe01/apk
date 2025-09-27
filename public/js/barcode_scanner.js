document.addEventListener('DOMContentLoaded', function () {
    const scannerButton = document.getElementById('start-scanner');
    const videoElement = document.getElementById('barcode-scanner');
    const resultsElement = document.getElementById('scan-results');

    scannerButton.addEventListener('click', () => {
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: videoElement,
            },
            decoder: {
                readers: ["code_128_reader", "ean_reader", "upc_reader"],
            },
        }, function (err) {
            if (err) {
                console.error(err);
                alert("Failed to initialize scanner");
                return;
            }
            Quagga.start();
        });

        Quagga.onDetected((data) => {
            const barcode = data.codeResult.code;
            Quagga.stop();
            videoElement.style.display = 'none';

            // Send the barcode to the backend API
            fetch(`/api/search?query=${barcode}`)
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        displayProduct(result.product);
                    } else {
                        resultsElement.textContent = "Product not found!";
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    resultsElement.textContent = "An error occurred while searching.";
                });
        });
    });
});

function displayProduct(product) {
    const resultsElement = document.getElementById('scan-results');
    resultsElement.innerHTML = `
        <h3>Product Details</h3>
        <p><strong>Name:</strong> ${product.name}</p>
        <p><strong>SKU:</strong> ${product.sku}</p>
        <p><strong>Barcode:</strong> ${product.barcode}</p>
        <p><strong>Category:</strong> ${product.category}</p>
        <p><strong>Location:</strong> ${product.location}</p>
        <p><strong>Expected Quantity:</strong> ${product.expected_quantity}</p>
        <p><strong>Actual Quantity:</strong> ${product.actual_quantity}</p>
    `;
}