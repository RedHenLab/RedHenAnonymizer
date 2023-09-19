var PENDING_FILES = [];
UPLOAD_URL='/upload';
NEXT_URL='/dashboard';
$(document).ready(function () {
    $("#uploader").on("click", function (e) {
        // console.log(e)
        if ($(e.target).is('#uploader')) {
            $(".file-input").click();
            $(".file-input").on("change", function () {
                // console.log("file-input clicked")
                handleFiles(this.files);
            })

        }
    });

    $(".button").on("click", function (e) {
        $("#progress").show();
        var $progressBar = $("#progress-bar");

        // Gray out the form.
        $("#upload-form :input").attr("disabled", "disabled");

        // Initialize the progress bar.
        $progressBar.css({ "width": "0%" });
        e.preventDefault();
        console.log("button-clicked")

        var all_inputs = $("#upload-form :input")
        console.log(all_inputs)

        // collect the form data
        var fd = new FormData();

        all_inputs.each(function () {
            var $this = $(this);
            var name = $this.attr("name");
            var type = $this.attr("type") || "";
            var value = $this.attr("value");
            if (type === "radio" && name === "visual_anonymization") {
                if ($this.is(":checked")) {
                    fd.append("visual_anonymization", value);
                    console.log(value, "visual_anonymization");
                }
            } else {
                if (name === 'pitch' || name === 'echo' || name === 'distortion') {
                    fd.append(name, $this.val());
                    console.log(name, $this.val());

                }
                if (name==='project_name'){
                    fd.append(name, $this.val());
                    console.log(name, $this.val());
                }
            }

        })

        //  attach the files
        for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
            fd.append("file", PENDING_FILES[i]);
            console.log(PENDING_FILES[i]);
        }

        fd.append("__ajax", "true");

        var xhr = $.ajax({
            xhr: function () {
                var xhrobj = $.ajaxSettings.xhr();
                if (xhrobj.upload) {
                    xhrobj.upload.addEventListener("progress", function (event) {
                        var percent = 0;
                        var position = event.loaded || event.position;
                        var total = event.total;
                        if (event.lengthComputable) {
                            percent = Math.ceil(position / total * 100);
                        }

                        // Set the progress bar.
                        $progressBar.css({ "width": percent + "%" });
                        $progressBar.text(percent + "%");
                    }, false)
                }
                return xhrobj;

            },
            url: UPLOAD_URL,
            method: "POST",
            contentType: false,
            processData: false,
            cache: false,
            data: fd,
            success: function (data) {
                $progressBar.css({ "width": "100%" });
                console.log("data", data);
                data = JSON.parse(data);

                // How'd it go?
                if (data.status === "error") {
                    // Uh-oh.
                    window.alert("Please enter files in correct format. Premissible formats are ['.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.m4p', '.m4v', '.avi', '.wmv']");
                    $("#upload-form :input").removeAttr("disabled");
                    window.location='/main';
                    return;
                }else{
                window.location=NEXT_URL;
                }

            },
        })
    })

});

function handleFiles(files) {
    for (var i = 0, ie = files.length; i < ie; i++) {
        PENDING_FILES.push(files[i]);
    }
}
