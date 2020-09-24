
$(function() {

    function make_row(gift_item) {
        // Use the red X emoji
        let delete_button = '<span class="delete" id="product_' + 
            gift_item.product._id  + '">&#x1F6AB;</span>';
        // Shopping bags
        let buy_button = '<span class="buy">&#x1F6CD;</span>'; 
        let purchase_status = buy_button + delete_button;
        // Tick emoji
        if(gift_item.purchased) {
            purchase_status = "&#x2714;";
        }

        return  '<tr id="product_' + gift_item.product._id  + '">'  +
            "<td>" + gift_item.product.name + "</td>" + 
            "<td>" + gift_item.product.brand + "</td>" + 
            "<td>£" + gift_item.product.price + "</td>" + 
            "<td>" + purchase_status + "</td>" + 
            "</tr>";
    }

    function update_table(gift_list) {
        let table = $("#gift_list");
        table.empty();
        gift_list.forEach(gift_item => 
            table.append(
                make_row(gift_item)
            )
        );
    }

    function product_id_for_row(element) {
        let product_id_str = element.closest('tr').attr("id");
        return product_id_str.split("_")[1];
    }

    function delete_gift() {
        $.ajax({
            type: 'DELETE',
            url: '/gifts/' + product_id_for_row($(this)) + '/',
            success: refresh
        });
    }

    function buy_gift() {
        $.ajax({
            type: 'PATCH',
            url: '/gifts/' + product_id_for_row($(this)) + '/',
            data: JSON.stringify({
                'purchase': true
            }),
            contentType: "application/json",
            dataType: 'json',
            success: refresh
        })
        product_id_for_row($(this))
    }

    function refresh() {
        $.getJSON("/gifts/", function(data) {
            update_table(data);
            $(".delete").click(delete_gift);
            $(".buy").click(buy_gift);
        });
    }

    refresh();
});