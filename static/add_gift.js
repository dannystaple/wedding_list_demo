$(function() {
    let product_table = $("#product_list");
    function make_row(product_item) {
        let stock_badge = "<td>0</td>";
        if(product_item.in_stock_quantity > 0) {
            stock_badge = "<td class=\"stock_badge\">" + product_item.in_stock_quantity + " in stock </td>";
        }

        return  "<tr id=\"product_" + product_item._id + "\">" + 
            "<td>" + product_item.name  + "</td>" + 
            "<td>" + product_item.brand  + "</td>" + 
            "<td>£" + product_item.price + "</td>" + 
            stock_badge + 
            "</tr>";
    }

    function update_table(gift_list) {
        product_table.empty();
        gift_list.forEach(gift_item => 
            product_table.append(
                make_row(gift_item)
            )
        );
    }

    function add_product() {
        let product_id = $( this ).attr("id").split("_")[1];
        $.ajax({
            type: 'POST',
            url: '/gifts/', 
            data: JSON.stringify({
                'product_id': parseInt(product_id)
            }), 
            contentType: "application/json",
            dataType: 'json',
            success: function() {
                window.location.href = '/';
            }
        });
    }

    $.getJSON("/products/", function(data) {
        update_table(data);
        product_table.find("tr").click(add_product);
    });
});