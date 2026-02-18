document.addEventListener("DOMContentLoaded", function () {


    document.querySelectorAll("input").forEach(function (tag) {
        tag.classList.add("form-control");
    });


    document.querySelectorAll("select").forEach(function (tag) {
        tag.classList.add("form-select");
    });


    document.querySelectorAll("textarea").forEach(function (tag) {
        tag.classList.add("form-control");
    });



    document.body.classList.add("loaded");

    document.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", function (e) {

            if (link.hostname === window.location.hostname) {
                e.preventDefault();

                document.body.classList.remove("loaded");

                setTimeout(() => {
                    window.location = link.href;
                }, 300);
            }
        });
    });

});
