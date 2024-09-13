$(() => {
    var $table =
        $("#stateProvinces")
            .DataTable({
                serverSide: true,
                processing: true,
                ajax: {
                    url: "/Table/StateProvinces",
                    data: function (d) {
                        if ($("#stateProvinces").data("$systemat") !== null)
                            d.$systemat = $("#stateProvinces").data("$systemat");
                    }
                },
                columns: [
                    { data: "StateProvinceName" },
                    { data: "StateProvinceCode" },
                    { data: "SalesTerritory", defaultContent: "" },
                    { data: "LatestRecordedPopulation", type: "numeric", defaultContent: "" },
                    { data: "CountryName", defaultContent: "" },
                    {
                        data: "StateProvinceID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        }
                    },
                    {
                        data: "StateProvinceID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-danger btn-sm delete"><span class="glyphicon glyphicon-trash"></span> Delete</button>';
                        }
                    }
                ]
            });

    var $form = $("#EditForm");
    var $dlg = $("#modalDialog");

    o('Countries')
        .select('CountryID,CountryName')
        .get(countries => $("#CountryID", $form).view(countries));

    $("button#add").on("click", e => $form[0].reset());

    $table.on("click", "button.edit",
        e => {
            $form[0].reset();
            var id = e.target.attributes["data-id"].value;
            o('StateProvinces')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the state.'));
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('StateProvinces')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The state is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the state.'));
        });

    $("button#save").on("click",
        e => {
            var id = $("#StateProvinceID", $form).val();
            var state = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('StateProvinces').find(id).put(state);
            } else {
                request = o('StateProvinces').post(state);
            }

            request
                .save()
                .then(model => {
                    toastr.success('The state is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the state.'));
        }
    );
});