$(document).ready(function () {

    setTimeout(function() {
        let alerts = document.querySelectorAll(".alert");
        alerts.forEach(a => {
            a.classList.remove("show");
            a.classList.add("fade");
            setTimeout(() => a.remove(), 300)
        });
    }, 1500);

    const uploadBtn = $('#uploadBtn');
    const clearBtn = $('#clearBtn');
    const fileInput = $('#fileInput');
    const previewContainer = $('#previewContainer');
    const dropZone = document.getElementById('dropZone');
    const hiddenPasteInput = document.getElementById('hiddenPasteInput'); 

    function disableDropZone() {
        dropZone.style.pointerEvents = "none";
        dropZone.style.opacity = "0.5";
    }
    function enableDropZone() {
        dropZone.style.pointerEvents = "auto";
        dropZone.style.opacity = "1";
    }
    function setInitialState() {
        uploadBtn.addClass('disabled-btn');
        clearBtn.addClass('disabled-btn');
        enableDropZone();
    }
    function setAfterFileSelected() {
        uploadBtn.removeClass('disabled-btn');
        clearBtn.removeClass('disabled-btn');
        disableDropZone();
    }
    function setAfterUploadConvert() {
        uploadBtn.addClass('disabled-btn');
        clearBtn.removeClass('disabled-btn');
        disableDropZone();
    }
    function setAfterClear() {
        uploadBtn.addClass('disabled-btn');
        clearBtn.addClass('disabled-btn');
        enableDropZone();
    }
    setInitialState();
    const hasUploaded = uploadBtn.data('has-uploaded') === 1 || uploadBtn.data('has-uploaded') === "1";
    if (hasUploaded) {
        uploadBtn.addClass('disabled-btn');
        disableDropZone();
    }
    function processFile(file) {
        if (file.size > 1 * 1024 * 1024) {
            Swal.fire({ icon: 'error', title: 'File size is too large' });
            return false;
        }
        if (file.type.indexOf("image") === -1) {
            Swal.fire({
                icon: 'warning',
                title: 'Format not supported',
                text: 'Can only be used for png, jpg, jpeg',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 1500
            });
            return false;
        }
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput[0].files = dataTransfer.files;
        const reader = new FileReader();
        reader.onload = function (event) {
            previewContainer.html(`
                <div class="text-center mt-3">
                    <img src="${event.target.result}" 
                         alt="Preview Gambar" 
                         class="img-fluid rounded shadow"
                         style="max-width: 400px; border: 2px solid #ddd;"/>
                </div>`);
        };
        reader.readAsDataURL(file);
        setAfterFileSelected();
        return true;
    }
    uploadBtn.on('click', function (e) {
        if ($(this).hasClass('disabled-btn')) {
            e.preventDefault();
            Swal.fire({
                icon: 'warning',
                title: 'The picture still exists',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 1500
            });
        } else {
            $("#fullscreenLoaded").css("display", "flex");
            $("body").css("overflow", "hidden");
            setAfterUploadConvert();
        }
    });
    fileInput.on('change', function (e) {
        const file = e.target.files[0];
        if (file) processFile(file);
    });
    clearBtn.on('click', function () {
        uploadBtn.removeClass('disabled-btn').data('has-uploaded', '0');
        fileInput.val('');
        previewContainer.empty();
        setAfterClear();
        Swal.fire({
            icon: 'success',
            title: 'Delete Success',
            text: 'Button upload active again',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 1500
        });
    });
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt => {
        dropZone.addEventListener(evt, e => e.preventDefault());
    });
    ['dragenter', 'dragover'].forEach(evt => {
        dropZone.addEventListener(evt, () => dropZone.classList.add('drop-zone-active'));
    });
    ['dragleave', 'drop'].forEach(evt => {
        dropZone.addEventListener(evt, () => dropZone.classList.remove('drop-zone-active'));
    });
    dropZone.addEventListener('drop', (e) => {
        if (uploadBtn.hasClass('disabled-btn') === false) {
            Swal.fire({
                icon: 'warning',
                title: 'The picture still exists!',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 1500
            });
            return;
        }
        const files = e.dataTransfer.files;
        if (files.length > 0) processFile(files[0]);
    });
    $(document).on('paste', function (e) {
        e.preventDefault(); 
        if (!uploadBtn.hasClass('disabled-btn')) {
             Swal.fire({
                icon:'warning',
                title: 'The picture still exists',
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 1500
            });
            return;
        }
        const clipboardItems = e.originalEvent.clipboardData.items;
        for (let i = 0; i < clipboardItems.length; i++){
            const item = clipboardItems[i];
            if(item.type.indexOf("image") !== -1){
                const file = item.getAsFile();
                processFile(file);
                return; 
            }
        }
        Swal.fire({
            icon: 'info',
            title: 'Paste failed',
            text: 'only images can be pasted',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000
        });
    });
    if (hiddenPasteInput && dropZone) {
        dropZone.addEventListener('contextmenu', function(e) {
            hiddenPasteInput.style.display = 'block';
            setTimeout(() => {
                hiddenPasteInput.focus();
                setTimeout(() => {
                    hiddenPasteInput.style.display = 'none'; 
                }, 100);
            }, 50); 
        });
        dropZone.addEventListener('click', function(e) {
            if (e.target !== fileInput[0]){
                if (hiddenPasteInput.style.display !== 'none') {
                    hiddenPasteInput.style.display = 'none';
                }
                fileInput.trigger('click');
            }
        });
    }
    $("#fullscreenLoaded").hide();
    $("body").css("overflow", "auto");
    if (uploaded_file){
        const img = $('#uploadedImage');
        const ocrLayer = $('#ocrLayer');

        function positionOverlays() {
            const origW = img[0].naturalWidth || img.width();
            const origH = img[0].naturalHeight || img.height();
            const dispW = img.width();
            const dispH = img.height();
            ocrLayer.find('.ocr-text').each(function () {
                const span = $(this);
                const x = parseFloat(span.data('x'));
                const y = parseFloat(span.data('y'));
                const w = parseFloat(span.data('w'));
                const h = parseFloat(span.data('h'));
                span.css({
                    left: x * dispW / origW,
                    top: y * dispH / origH,
                    width: w * dispW / origW,
                    height: h * dispH / origH
                });
            });
            ocrLayer.css({ width: dispW, height: dispH });
        }
        if (img[0].complete) {
            positionOverlays();
        } else {
            img.on('load', positionOverlays);
        }
        $(window).on('resize', function () {
            setTimeout(positionOverlays, 150);
        });
        const imageModal = new bootstrap.Modal($('#imageModal')[0]);
        imageModal.show();
        $('#imageModal').on('shown.bs.modal', positionOverlays);
    }
    $('#imageModal').on('hidden.bs.modal', function () {
        uploadBtn.addClass('disabled-btn');
        clearBtn.removeClass('disabled-btn');
        disableDropZone();
    })
});
