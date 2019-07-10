function doModal (url) {

    jQuery('#modal_frame').modal({
        overlayClose: true, 
        onClose: function () {location.reload()},
        onShow: function () {document.getElementById("modal_frame").src = url}
    })
}

function doModal2 (url) {

    jQuery('#modal_frame').modal({
        overlayClose: true, 
        onShow: function () {document.getElementById("modal_frame").src = url}
    })
}