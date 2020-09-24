
$(function() {

    function make_row(gift_item) {
        return $.html(
            "<tr><td>" + gift_item.product.name +
            "</tr></td>"
        )
    }

    function update_table(gift_list) {
        table = $("#gift-list");
        table.empty()
        gift_list.forEach(gift_list, function(gift_item) {
            table.append(
                make_row(gift_item)
            );
        });
    }

    data = $.getJSON("/gifts/",
        function(data) {
            update_table(data);
        });
    
});