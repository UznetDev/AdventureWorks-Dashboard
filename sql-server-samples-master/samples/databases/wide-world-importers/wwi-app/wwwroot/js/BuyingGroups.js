$(() => {
    var $table =
        $("#buyingGroups")
            .DataTable({
                "ajax": {
                    "url": "/OData/BuyingGroups",
                    "dataSrc": "value"
                },
                "columns": [
                    { data: "BuyingGroupName" },
                    {
                        data: "BuyingGroupID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        },
                        width: "100px"
                    },
                    {
                        data: "BuyingGroupID",
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
            o('BuyingGroups')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the buying group.') );
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('BuyingGroups')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The buying group is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the buying group.'));
        });

    $("button#save").on("click",
        e => {
            var id = $("#BuyingGroupID", $form).val();
            var model = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('BuyingGroups').find(id).put(model);
            } else {
                request = o('BuyingGroups').post(model);
            }

            request
                .save()
                .then(e => {
                    toastr.success('The buying group is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the buying group.'));
        }
    );
});