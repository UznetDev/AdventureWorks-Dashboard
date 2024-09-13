$(() => {
    // Transition rules
    $("body")
        .on("open-order-edit", e => {
            $(".order-list").addClass("hidden");
            $(".order-edit").removeClass("hidden");
            window.scrollTo(0, 0);
        })
        .on("close-order-edit", e => {
            $(".order-list").removeClass("hidden");
            $(".order-edit").addClass("hidden");
            window.scrollTo(0, 0);
        });
});