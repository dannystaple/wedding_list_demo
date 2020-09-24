
$(function() {

    function make_row(gift_item) {
        let purchase_status = "";
        if(gift_item.purchased) {
            purchase_status = "✔️";
        }

        return  "<tr>"  + 
            "<td>" + gift_item.product.name + "</td>" + 
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

    data = $.getJSON("/gifts/",
        function(data) {
            update_table(data);
        });
    
});