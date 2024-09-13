$(() => {
    var $table =
        $("#deliveryMethods")
            .DataTable({
                "ajax": {
                    "url": "/OData/DeliveryMethods",
                    "dataSrc": "value"
                },
                "columns": [
                    { data: "DeliveryMethodName" },
                    {
                        data: "DeliveryMethodID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        }
                    },
                    {
                        data: "DeliveryMethodID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-danger btn-sm delete glyphicon glyphicon-trash"> Delete</button>';
                        }
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
            o('DeliveryMethods')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the delivery method.') );
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('DeliveryMethods')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The delivery method is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the delivery method.'));
        });

    $("button#save").on("click",
        e => {
            var id = $("#DeliveryMethodID", $form).val();
            var model = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('DeliveryMethods').find(id).put(model);
            } else {
                request = o('DeliveryMethods').post(model);
            }

            request
                .save()
                .then(e => {
                    toastr.success('The delivery method is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the delivery method.'));
        }
    );
});