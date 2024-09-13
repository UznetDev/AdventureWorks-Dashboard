$(() => {
    $("#customerTransactions")
        .DataTable({
            ajax: "/Table/CustomerTransactions",
            serverSide: true,
            processing: true,
            "columns": [
                { data: "TransactionDate" },
                { data: "TransactionAmount", defaultContent: "" },
                { data: "IsFinalized", defaultContent: "" },
                { data: "CustomerName", defaultContent: "" },
                { data: "TransactionTypeName", defaultContent: "" },
                { data: "PaymentMethodName", defaultContent: "" },
                {
                    data: "CustomerTransactionID",
                    "sortable": false,
                    "searchable": false,
                    "render": function (data) {
                        return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalCustomerTransactionDialog"> Edit</button>';
                    }
                }
            ]
        });
});