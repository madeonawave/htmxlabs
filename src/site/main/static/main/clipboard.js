
// Clipboard utility for copying HTML (and plain text) from .bd-clipboard elements

function copyClipboardContent(btn) {
    // Find the closest .box parent
    var box = btn.closest('.box');
    // Find the first .bd-clipboard inside the box that is NOT the button's own container
    var clips = box.querySelectorAll('.bd-clipboard');
    var target = null;
    for (var i = 0; i < clips.length; i++) {
        if (!clips[i].contains(btn)) {
            target = clips[i];
            break;
        }
    }
    // If not found, fallback to the first <code> inside the box
    if (!target) {
        target = box.querySelector('code');
    }
    if (target) {
        // Copy the HTML content (including tags) to the clipboard
        var html = target.innerHTML.trim();
        // Use Clipboard API with both text and HTML
        if (navigator.clipboard && window.ClipboardItem) {
            var blobInput = [
                new ClipboardItem({
                    "text/html": new Blob([html], { type: "text/html" }),
                    "text/plain": new Blob([html], { type: "text/plain" })
                })
            ];
            navigator.clipboard.write(blobInput).then(function() {
                btn.classList.add('is-success');
                btn.querySelector('span:last-child').textContent = 'Copied!';
                setTimeout(function() {
                    btn.classList.remove('is-success');
                    btn.querySelector('span:last-child').textContent = 'Copy';
                }, 1200);
            });
        } else {
            // Fallback: copy as plain text
            var textarea = document.createElement('textarea');
            textarea.value = html;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            btn.classList.add('is-success');
            btn.querySelector('span:last-child').textContent = 'Copied!';
            setTimeout(function() {
                btn.classList.remove('is-success');
                btn.querySelector('span:last-child').textContent = 'Copy';
            }, 1200);
        }
    }
}

