$(() => {
    var $table =
        $("#countries")
            .DataTable({
                serverSide: true,
                processing: true,
                ajax: {
                    url: "/Table/Countries",
                    data: function (d) {
                        if ($("#countries").data("$systemat") !== null)
                            d.$systemat = $("#countries").data("$systemat");
                    }
                },
                "columns": [
                    { data: "FormalName" },
                    { data: "Subregion", defaultContent: "" },
                    { data: "Region", defaultContent: "" },
                    { data: "Continent", defaultContent: "" },
                    { data: "LatestRecordedPopulation", type: "numeric", defaultContent: "" },
                    {
                        data: "CountryID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        }
                    },
                    {
                        data: "CountryID",
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
            o('Countries')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the country.'));
        });

    $table.on("click", "button.delete",
        e => {
            try {
                var id = e.target.attributes["data-id"].value;
                o('Countries')
                    .find(id).remove()
                    .save()
                    .then(model => {
                        toastr.success('The country is successfully deleted.');
                        $table.ajax.reload();
                    })
                    .fail(e => toastr.error('An error occured while trying to delete the country.'));
            } catch (ex) {
                alert(ex);
            }
        });

    $("button#save").on("click",
        e => {
            var id = $("#CountryID", $form).val();
            var city = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('Countries').find(id).put(city);
            } else {
                request = o('Countries').post(city);
            }

            request
                .save()
                .then(model => {
                    toastr.success('The country is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the country.'));
        }
    );
});