$(() => {
    var $table =
        $("#stockGroups")
            .DataTable({
                "ajax": {
                    "url": "/OData/StockGroups",
                    "dataSrc": "value"
                },
                "columns": [
                    { data: "StockGroupName" },
                    {
                        data: "StockGroupID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        },
                        width: "100px"
                    },
                    {
                        data: "StockGroupID",
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
            o('StockGroups')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the stock group.') );
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('StockGroups')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The stock group is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the stock group.'));
        });

    $("button#save").on("click",
        e => {
            var id = $("#StockGroupID", $form).val();
            var model = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('StockGroups').find(id).put(model);
            } else {
                request = o('StockGroups').post(model);
            }

            request
                .save()
                .then(e => {
                    toastr.success('The stock group is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the stock group.'));
        }
    );
});