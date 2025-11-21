$(window).on('load', function () {
    const defaultIcon = $('#default-icon-contact-details');
    const successIcon = $('#success-icon-contact-details');
    const defaultTooltipMessage = $('#default-tooltip-message-contact-details');
    const successTooltipMessage = $('#success-tooltip-message-contact-details');
    const tooltip = $('#tooltip-ocrResult');
    $('#btn-copy').on('click', function () {
        const text = $('#ocrResult').val();
        navigator.clipboard.writeText(text).then(function () {
            showSuccess();
            setTimeout(() => {
                resetToDefault();
            }, 2000);
        });
    });
    
    function showSuccess() {
        defaultIcon.addClass('hidden');
        successIcon.removeClass('hidden');
        successIcon.addClass('text-blue-500');
        defaultTooltipMessage.addClass('hidden');
        successTooltipMessage.removeClass('hidden');
        successTooltipMessage.addClass('text-blue-500');
        tooltip.removeClass('invisible opacity-0').addClass('visible opacity-100');
    }

    function resetToDefault() {
        defaultIcon.removeClass('hidden');
        successIcon.addClass('hidden');
        successIcon.removeClass('text-blue-500');
        defaultTooltipMessage.removeClass('hidden');
        successTooltipMessage.addClass('hidden');
        successTooltipMessage.removeClass('text-blue-500');
        tooltip.addClass('invisible opacity-0').removeClass('visible opacity-100');
    }
});
        const conmodal = $("#conmodal");
        const modalbox = $("#modalbox");
        const closebtn = $("#btn-close");
        let dropLock = false;

        function openModal(){
            conmodal.removeClass("opacity-0 invisible");
            modalbox.removeClass("opacity-0 scale-95").addClass("opacity-100 scale-100");
            dropLock = true;
        };
        function closeModal(){
            conmodal.addClass("opacity-0 invisible");
            modalbox.removeClass("opacity-0 scale-100").addClass("opacity-0 scale-95");
            dropLock = false;
        };
        closebtn.on("click", closeModal);

        conmodal.on("click", function(e){
            if (e.target === this) return;
        })
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
    function enableButton(btn) {
    btn.removeAttr("disabled")
       .removeClass("opacity-50 cursor-not-allowed")
       .addClass("cursor-pointer");
}
function disableButton(btn) {
    btn.attr("disabled", true)
       .removeClass("cursor-pointer")
       .addClass("opacity-50 cursor-not-allowed");
}
    function setInitialState() {
    disableButton(uploadBtn);
    disableButton(clearBtn);
    enableDropZone();
}
    function setAfterFileSelected() {
    enableButton(uploadBtn);
    enableButton(clearBtn);
    disableDropZone();
}
    function setAfterUploadConvert() {
    disableButton(uploadBtn);
    enableButton(clearBtn);
    disableDropZone();
}
    function setAfterClear() {
    disableButton(uploadBtn);
    disableButton(clearBtn);
    enableDropZone();
}
    setInitialState();
    const hasUploaded = uploadBtn.data('has-uploaded') === 1 || uploadBtn.data('has-uploaded') === "1";
    if (hasUploaded) {
        uploadBtn.addClass('opacity-50 cursor-not-allowed').attr('disabled', true);
        disableDropZone();
    }
    function processFile(file) {
        if (file.size > 1 * 1024 * 1024) {
            Swal.fire({ icon: 'error', title: 'File size is too large', position: 'top-end', showConfirmButton: false, timer: 1500, toast: true });
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
                <div class="flex justify-center mt-3">
                    <img src="${event.target.result}" alt="Preview Gambar" class="max-w-xs rounded shadow-md border-2 border-gray-200"/>
                </div>`);
        };
        reader.readAsDataURL(file);
        setAfterFileSelected();
        return true;
    }
   uploadBtn.on('click', function (e) {
    if ($(this).prop('disabled')) {
        e.preventDefault();
        Swal.fire({
            icon: 'warning',
            title: 'The picture still exists',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 1500
        });
        return;
    }
    e.preventDefault();
    $("#fullscreenLoaded").removeClass("hidden").addClass("flex");
    $("body").addClass("overflow-hidden");
    setAfterUploadConvert();
    setTimeout(() => {
        $(this).closest("form").submit();
    }, 300);
});
        closebtn.on('click', function () {
            $("#fullscreenLoaded").removeClass("hidden").addClass("flex");
            $("body").addClass("overflow-hidden");
        })
    fileInput.on('change', function (e) {
        const file = e.target.files[0];
        if (file) processFile(file);
    });
    clearBtn.on('click', function () {
        uploadBtn.removeClass('opacity-50 cursor-not-allowed').data('has-uploaded', '0');
        fileInput.val('');
        previewContainer.empty();
        setAfterClear();
        Swal.fire({
            icon: 'success',
            title: 'Delete Success',
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
    if(dropLock) return;
    if (!uploadBtn.prop('disabled')) {
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
        if(dropLock) {
            e.preventDefault();
            return;
        }
        e.preventDefault(); 
        if (!uploadBtn.hasClass('opacity-50 cursor-not-allowed')) {
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
    $("#fullscreenLoaded").addClass("hidden");
    $("body").removeClass("overflow-hidden");
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
        openModal();
        setTimeout(positionOverlays, 50);
    }
    conmodal.on("tansitionend", function () {
        if (conmodal.hasClass("invisible")){
            uploadBtn.addClass('opacity-50 cursor-not-allowed').attr('disabled', true);;
            clearBtn.removeClass('opacity-50 cursor-not-allowed').attr('disabled', true);;
            disableDropZone();
        }
    });
});
