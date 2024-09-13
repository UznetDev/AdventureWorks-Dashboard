$(() => {
    $("#orders").DataTable({
        ajax: { url: "/OData/PurchaseOrders?$top=0", dataSrc: "value" },
        processing: true,
        columns: [
            { data: "OrderDate" },
            { data: "SupplierReference", defaultContent: "", visible: false },
            { data: "ExpectedDeliveryDate", defaultContent: "" },
            { data: "ContactName", defaultContent: "" },
            { data: "ContactPhone", defaultContent: "" },
            { data: "IsOrderFinalized", defaultContent: "" },
            {
                data: "PurchaseOrderID",
                sortable: false,
                searchable: false,
                render: function (data) {
                    return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit"> Edit</button>';
                }
            }
        ]
    });
});