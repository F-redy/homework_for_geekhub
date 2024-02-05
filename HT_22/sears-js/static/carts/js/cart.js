$(document).ready(function () {

    // Ловим клик по добавлению товара в корзину
    $('#add-to-cart').on('click', function (evt) {
        evt.preventDefault();
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();
        const addToCartUrl = $(this).data("add-product-url");
        $.ajax({
            type: 'POST',
            url: addToCartUrl,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (data) {
                showNotification(data);
            },
            error: function (data) {
                console.log(data);
            },
        });

    });

    // Ловим клики по + или -
    $('.decrement-btn, .increment-btn').on('click', function (evt) {
        evt.preventDefault();
        const productUrl = $(this).data('product-url');
        const action = $(this).data('action');
        const quantity = $(this).data('quantity')

        updateCartQuantity(productUrl, action, quantity)
    });

    // Ловим ввод quantity, после нажатия Enter
    $('.quantity').on('keydown', function (evt) {
        if (evt.key === 'Enter') {
            const productUrl = $(this).data('product-url');
            const action = $(this).data('action');
            const quantity = $(this).val();

            // Проверка на целое положительное число
            if (/^\d+$/.test(quantity) && parseInt(quantity, 10) > -1 && parseInt(quantity, 10) <  101) {
                updateCartQuantity(productUrl, action, quantity);
            } else {
                showNotification({'notification': 'The quantity must be between 0 and 100.'});
            }
        }
    });

    // Ловим клик по кнопке удалить товар из корзины
    $('.remove-from-cart').on("click", function (evt) {
        evt.preventDefault();

        const cartUrl = $(this).data("cart-url");
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: 'DELETE',
            url: cartUrl,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (data) {
                let cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
                showNotification(data);
            },
            error: function (data) {
                console.log(data);
            },
        });
    });

    // Ловим клик по кнопке очистить корзину
    $('#clear-basket').on('click', function (evt) {
        evt.preventDefault();
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();
        const deleteUrl = $(this).data("delete-url");

        $.ajax({
            type: 'DELETE',
            url: deleteUrl,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function (data) {
                let cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
                showNotification(data);
            },
            error: function (data) {
                console.log(data);
            },
        });
    });
});

function updateCartQuantity(productUrl, action, quantity) {
    if (quantity > -1 && quantity < 101) {
        if (quantity === 0 && action === 'sub') {
            showNotification({'notification': 'The quantity must be greater than 0.'})
        } else if (quantity === 100 && action === 'add') {
            showNotification({'notification': 'The quantity must be less than or equal to 100.'});
        } else {

            const csrfToken = $("[name=csrfmiddlewaretoken]").val();

            $.ajax({
                type: 'POST',
                url: productUrl,
                data: {
                    'action': action,
                    'quantity': quantity,
                },
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
                },
                success: function (data) {
                    let cartItemsContainer = $("#cart-items-container");
                    cartItemsContainer.html(data.cart_items_html);
                    showNotification(data);
                },
            });
        }
    } else {
        showNotification({'notification': 'The quantity must be between 0 and 100.'})
    }
}

function showNotification(data) {
    // Добавление класса в зависимости от сообщения
    if (data.notification) {
        let notification = $('.jq-notification');
        notification.html(data.notification).removeClass('alert-error alert-success');
        if (data.success) {
            notification.addClass('alert-success').fadeIn(400);
        } else {
            notification.addClass('alert-error').fadeIn(400);
        }
        // Скрытие уведомления через 5 секунд
        setTimeout(function () {
            notification.fadeOut(400);
        }, 5000);
    }
}
