$(() => {
        $("#orders")
            .DataTable({
                ajax: "/Table/SalesOrders",
                serverSide: true,
                processing: true,
                columns: [
                    { data: "OrderDate" },
                    { data: "CustomerPurchaseOrderNumber", defaultContent: "" },
                    { data: "CustomerName", defaultContent: "" },
                    { data: "ExpectedDeliveryDate", defaultContent: "" },
                    { data: "PhoneNumber", defaultContent: "" },
                    { data: "SalesPerson", defaultContent: "" },
                    {
                        data: "OrderID",
                        sortable: false,
                        searchable: false,
                        render: function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit"> Edit</button>';
                        }
                    }
                ]
            });
});