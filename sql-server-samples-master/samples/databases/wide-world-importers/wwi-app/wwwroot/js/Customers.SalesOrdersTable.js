$(() => {
        $("#orders")
            .DataTable({
                ajax: {
                    url: "/OData/SalesOrders?$top=0",
                    dataSrc: "value"
                },
                columns: [
                    { data: "OrderDate" },
                    { data: "CustomerPurchaseOrderNumber", defaultContent: "" },
                    { data: "CustomerName", defaultContent: "", visible: false },
                    { data: "ExpectedDeliveryDate", defaultContent: "" },
                    { data: "PhoneNumber", defaultContent: "" },
                    { data: "SalesPerson", defaultContent: "" },
                    {
                        data: "OrderID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        }
                    }
                ]
            });
});