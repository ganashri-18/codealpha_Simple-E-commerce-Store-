document.addEventListener(
    "DOMContentLoaded",
    function () {

        const messages =
            document.querySelectorAll(
                ".message"
            );

        setTimeout(function () {

            messages.forEach(
                function (message) {

                    message.style.opacity = "0";

                }
            );

        }, 3000);

    }
);