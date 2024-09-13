$(() => {
    $("#stockItems")
        .DataTable({
            serverSide: true,
            processing: true,
            ajax: {
                url: "/Table/StockItems",
                data: function (d) {
                    if ($("#stockItems").data("$systemat") !== null)
                        d.$systemat = $("#stockItems").data("$systemat");
                }
            },
            columns: [
                { data: "StockItemName" },
                { data: "SupplierName", defaultContent: "" },
                { data: "UnitPrice", defaultContent: "" },
                { data: "TaxRate", defaultContent: "" },
                { data: "RecommendedRetailPrice", defaultContent: "" },
                {
                    data: "StockItemID",
                    "sortable": false,
                    "searchable": false,
                    "render": function (data) {
                        return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalStockItemDialog"> Edit</button>';
                    }
                },
                {
                    data: "StockItemID",
                    "sortable": false,
                    "searchable": false,
                    "render": function (data) {
                        return '<button data-id="' + data + '" class="btn btn-danger btn-sm delete"><span class="glyphicon glyphicon-trash"></span> Delete</button>';
                    }
                }
            ]
        });
});