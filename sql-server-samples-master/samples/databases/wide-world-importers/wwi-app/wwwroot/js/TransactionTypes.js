$(() => {
    var $table =
        $("#transactionTypes")
            .DataTable({
                "ajax": {
                    "url": "/OData/TransactionTypes",
                    "dataSrc": "value"
                },
                "columns": [
                    { data: "TransactionTypeName" },
                    {
                        data: "TransactionTypeID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        },
                        width: "100px"
                    },
                    {
                        data: "TransactionTypeID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-danger btn-sm delete glyphicon glyphicon-trash"> Delete</button>';
                        },
                        width: "100px"
                    }
                ]
            });

    var $form = $("#EditForm");
    var $dlg = $("#modalDialog");

    $("button#add").on("click", e => $form[0].reset());

    $table.on("click", "button.edit",
        e => {
            $form[0].reset();
            var id = e.target.attributes["data-id"].value;
            o('TransactionTypes')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the transaction type.') );
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('TransactionTypes')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The transaction type is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the transaction type.'));
        });

    $("button#save").on("click",
        e => {
            var id = $("#TransactionTypeID", $form).val();
            var model = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('TransactionTypes').find(id).put(model);
            } else {
                request = o('TransactionTypes').post(model);
            }

            request
                .save()
                .then(e => {
                    toastr.success('The transaction type is successfully saved.');
                    $table.ajax.reload();
                    $dlg.modal('hide');
                })
                .fail(e => toastr.error('An error occured while trying to save the transaction type.'));
        }
    );
});