$(() => {

    var $table = $("#orders").DataTable();
    var $orderLines =
        $("#orderLines")
            .DataTable({
                ajax: {
                    url: "/OData/PurchaseOrderLines?$filter=PurchaseOrderLineID eq -1",
                    dataSrc: "value"
                },
                columns: [
                    { data: "Description" },
                    { data: "OrderedOuters", defaultContent: "" },
                    { data: "ExpectedUnitPricePerOuter", defaultContent: "" },
                    { data: "ReceivedOuters", defaultContent: "" },
                    { data: "ProductName", defaultContent: "" },
                    { data: "IsOrderLineFinalized", defaultContent: "" },
                    { data: "PackageTypeName", defaultContent: "" }
                ]
            });

    var $formOrder = $("#EditPurchaseOrderForm");

    o('DeliveryMethods')
        .select('DeliveryMethodID,DeliveryMethodName')
        .get(list => $("#DeliveryMethodID", $formOrder).view(list));

    $("button#add").on("click", e => $formOrder[0].reset());

    $table.on("click", "button.edit",
        e => {
            $formOrder[0].reset();
            var id = e.target.attributes["data-id"].value;
            o('PurchaseOrders')
                .find(id)
                .get()
                .then(model => {
                    $orderLines.clear().draw();
                    $("body").trigger("open-order-edit");
                    $formOrder.view(model.data);
                    $orderLines.ajax.url("/OData/PurchaseOrderLines?$top=100&$filter=PurchaseOrderID eq " + id);
                    $orderLines.ajax.reload();
                })
                .fail(e => {
                    toastr.error('An error occured while trying to get the purchase order.');
                });
        });

    $("button#save").on("click",
        e => {
            var id = $("#PurchaseOrderID", $formOrder).val();
            var state = $formOrder.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('PurchaseOrders').find(id).put(state);
            } else {
                request = o('PurchaseOrders').post(state);
            }

            request
                .save()
                .then(model => {
                    toastr.success('The purchase order is successfully saved.');
                    $table.ajax.reload();
                    $("body").trigger("close-order-edit");
                })
                .fail(e => toastr.error('An error occured while trying to save the purchase order.'));
        });
    $("button#cancel").on("click",
        e => {
            $("body").trigger("close-order-edit");
        });
});