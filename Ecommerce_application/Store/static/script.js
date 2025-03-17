$(document).ready(function () {
    $(".increment-btn").click(function (e) {
        e.preventDefault();
        let $row = $(this).closest(".card");
        let value = parseInt($row.find(".quantity-input").val(), 10) || 0;
        let maxStock = parseInt($row.find(".quantity-input").attr("data-max-stock"));
    
        if (value < maxStock) {
            value++;
            $row.find(".quantity-input").val(value); 
            $row.find(".error-message").hide(); 
        } else {
            $row.find(".error-message")
                .text(`Only ${maxStock} quantities are available.`)
                .show(); 
        }
    });
    
    $(".decrement-btn").click(function (e) {
        e.preventDefault();

        let $row = $(this).closest(".card");
        let dec_value = $row.find(".quantity-input").val();
        let value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
    
        if (value > 1) {
            value--;
            $row.find(".quantity-input").val(value); 
            $row.find(".error-message").hide(); 
        }
    });
    
    
    function updateCartTotal() {
        let total = 0;
        $(".card").each(function () {
            let productTotal = parseFloat($(this).find(".product-price").text().replace('Rs ', ''));
            total += productTotal;
        });

        // Update the cart total in the DOM
        $(".cart-total").text('Total: Rs ' + total.toFixed(2));
    }

    // Handle delete button click and remove product from cart
    $(".delete-btn").click(function(e){
        e.preventDefault();
        var product_id = $(this).closest(".card").find(".prod_id").val();
        var token = $("input[name=csrfmiddlewaretoken]").val();
        var row = $(this).closest('tr');
    
        $.ajax({
            method: "POST",
            url: "/delete-cart-item",  // Ensure this URL matches the path in urls.py
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function(response){
                alertify.dismissAll(); 
                if(response.status === 'deleted successfully'){
                    alertify.success(response.status,1);
                    row.fadeOut(600, function() {
                        $(this).remove();
                        updateCartTotal();  // Update cart total after removing item
                    });
                } 
            }
        });
    });
});

    // Add to cart event listener
    // Add to cart event listener for all buttons with class 'add-to-cart-btn'
    $(document).ready(function() {
        $(".add-to-cart-btn").click(function (e) {
            e.preventDefault();
    
            // Find the closest product card and get the hidden values
            let $row = $(this).closest('.products-card, .trending-products, .card');
            let product_id = $row.find('.prod_id').val();
            let product_qty = $row.find('.quantity-input').val();
            let token = $('input[name=csrfmiddlewaretoken]').val();
            let messageBox = $("#cart-message"); // Error message div (Make sure you add this in HTML)
    
            $.ajax({
                method: "POST",
                url: "/add-to-cart",
                data: {
                    'product_id': product_id,
                    'product_qty': product_qty,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    alertify.dismissAll(); // Clear any existing notifications
                    
                    if (response.status.includes("out of stock") || response.status.includes("Only")) {
                        messageBox.css("color", "red").text(response.status).fadeIn(); // Show error in red
                        alertify.error(response.status); // Show error notification
                    } else {
                        messageBox.css("color", "green").text(response.status).fadeIn(); // Show success in green
                        alertify.success(response.status); // Show success notification
                    }
                },
                error: function () {
                    alertify.error("Error adding product to cart.");
                }
            });
        });
      
    $(".changequantity").click(function (e) {
        e.preventDefault();

        // Find the closest product card and get the hidden values
        let product_id = $(this).closest('.card').find('.prod_id').val();
        let product_qty = $(this).closest('.card').find('.quantity-input').val();
        let token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
          
        });
    });
});




    
   