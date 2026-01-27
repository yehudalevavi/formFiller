// PDF Form Filler - Client-side JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pdfForm');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error-message');

    // PDF Upload elements
    const pdfUpload = document.getElementById('pdfUpload');
    const fileNameSpan = document.getElementById('fileName');
    const browseBtn = document.getElementById('browseBtn');
    const uploadStatus = document.getElementById('uploadStatus');
    const uploadError = document.getElementById('uploadError');

    // Signature pad elements
    const signatureCanvas = document.getElementById('signaturePad');
    const clearSignatureBtn = document.getElementById('clearSignature');
    let signatureCtx = null;
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    // Track uploaded file and validation state
    let uploadedPdfFile = null;
    let pdfValidated = false;

    // Initialize signature pad
    if (signatureCanvas) {
        initSignaturePad();
    }

    // File upload handling
    if (pdfUpload) {
        pdfUpload.addEventListener('change', async function(e) {
            const file = e.target.files[0];

            if (!file) {
                resetUploadState();
                return;
            }

            // Update file name display
            fileNameSpan.textContent = file.name;
            fileNameSpan.classList.add('has-file');
            uploadedPdfFile = file;
            pdfValidated = false;

            // Validate the uploaded PDF
            await validateUploadedPdf(file);
        });

        // Allow clicking on browse button to trigger file input
        if (browseBtn) {
            browseBtn.addEventListener('click', function(e) {
                e.preventDefault();
                pdfUpload.click();
            });
        }
    }

    // Signature pad functionality
    function initSignaturePad() {
        signatureCtx = signatureCanvas.getContext('2d');

        // Set up canvas size based on container
        resizeSignatureCanvas();
        window.addEventListener('resize', resizeSignatureCanvas);

        // Set drawing styles
        signatureCtx.strokeStyle = '#000';
        signatureCtx.lineWidth = 2;
        signatureCtx.lineCap = 'round';
        signatureCtx.lineJoin = 'round';

        // Mouse events
        signatureCanvas.addEventListener('mousedown', startDrawing);
        signatureCanvas.addEventListener('mousemove', draw);
        signatureCanvas.addEventListener('mouseup', stopDrawing);
        signatureCanvas.addEventListener('mouseout', stopDrawing);

        // Touch events
        signatureCanvas.addEventListener('touchstart', handleTouchStart, { passive: false });
        signatureCanvas.addEventListener('touchmove', handleTouchMove, { passive: false });
        signatureCanvas.addEventListener('touchend', stopDrawing);
        signatureCanvas.addEventListener('touchcancel', stopDrawing);

        // Clear button
        if (clearSignatureBtn) {
            clearSignatureBtn.addEventListener('click', clearSignature);
        }
    }

    function resizeSignatureCanvas() {
        const container = signatureCanvas.parentElement;
        const rect = container.getBoundingClientRect();

        // Store current signature if any
        const imageData = signatureCtx ? signatureCanvas.toDataURL() : null;

        // Set canvas size to match container width
        const dpr = window.devicePixelRatio || 1;
        signatureCanvas.width = rect.width * dpr;
        signatureCanvas.height = 150 * dpr;

        // Scale for high DPI displays
        signatureCtx = signatureCanvas.getContext('2d');
        signatureCtx.scale(dpr, dpr);

        // Set drawing styles after resize
        signatureCtx.strokeStyle = '#000';
        signatureCtx.lineWidth = 2;
        signatureCtx.lineCap = 'round';
        signatureCtx.lineJoin = 'round';

        // Restore signature if it existed
        if (imageData && imageData !== 'data:,') {
            const img = new Image();
            img.onload = function() {
                signatureCtx.drawImage(img, 0, 0, rect.width, 150);
            };
            img.src = imageData;
        }
    }

    function getCanvasCoordinates(e) {
        const rect = signatureCanvas.getBoundingClientRect();
        let clientX, clientY;

        if (e.touches && e.touches.length > 0) {
            clientX = e.touches[0].clientX;
            clientY = e.touches[0].clientY;
        } else {
            clientX = e.clientX;
            clientY = e.clientY;
        }

        return {
            x: clientX - rect.left,
            y: clientY - rect.top
        };
    }

    function startDrawing(e) {
        isDrawing = true;
        const coords = getCanvasCoordinates(e);
        lastX = coords.x;
        lastY = coords.y;
    }

    function draw(e) {
        if (!isDrawing) return;

        const coords = getCanvasCoordinates(e);

        signatureCtx.beginPath();
        signatureCtx.moveTo(lastX, lastY);
        signatureCtx.lineTo(coords.x, coords.y);
        signatureCtx.stroke();

        lastX = coords.x;
        lastY = coords.y;
    }

    function stopDrawing() {
        isDrawing = false;
    }

    function handleTouchStart(e) {
        e.preventDefault();
        startDrawing(e);
    }

    function handleTouchMove(e) {
        e.preventDefault();
        draw(e);
    }

    function clearSignature() {
        const rect = signatureCanvas.getBoundingClientRect();
        signatureCtx.clearRect(0, 0, rect.width, 150);
    }

    function isSignatureEmpty() {
        const rect = signatureCanvas.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        const imageData = signatureCtx.getImageData(0, 0, rect.width * dpr, 150 * dpr);
        const data = imageData.data;

        // Check if all pixels are transparent
        for (let i = 3; i < data.length; i += 4) {
            if (data[i] !== 0) {
                return false;
            }
        }
        return true;
    }

    function getSignatureDataUrl() {
        if (isSignatureEmpty()) {
            return null;
        }
        return signatureCanvas.toDataURL('image/png');
    }

    // Validate uploaded PDF
    async function validateUploadedPdf(file) {
        showUploadStatus('validating', 'מאמת את קובץ ה-PDF...');
        hideUploadError();

        const formData = new FormData();
        formData.append('pdf_file', file);

        try {
            const response = await fetch('/api/validate-pdf', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.valid) {
                pdfValidated = true;
                let message = 'קובץ PDF תקין';
                if (result.warnings && result.warnings.length > 0) {
                    message += ' (עם אזהרות)';
                }
                showUploadStatus('valid', message);

                if (result.warnings && result.warnings.length > 0) {
                    console.log('PDF validation warnings:', result.warnings);
                }
            } else {
                pdfValidated = false;
                showUploadStatus('invalid', 'קובץ PDF לא תקין');
                showUploadError(result.errors || result.details || ['שגיאה לא ידועה']);
            }
        } catch (error) {
            console.error('Validation error:', error);
            pdfValidated = false;
            showUploadStatus('invalid', 'שגיאה באימות הקובץ');
            showUploadError([error.message || 'שגיאה בבדיקת הקובץ']);
        }
    }

    function resetUploadState() {
        uploadedPdfFile = null;
        pdfValidated = false;
        fileNameSpan.textContent = 'לא נבחר קובץ';
        fileNameSpan.classList.remove('has-file');
        hideUploadStatus();
        hideUploadError();
    }

    function showUploadStatus(status, message) {
        uploadStatus.className = 'upload-status ' + status;
        uploadStatus.querySelector('.status-message').textContent = message;
        uploadStatus.style.display = 'flex';
    }

    function hideUploadStatus() {
        uploadStatus.style.display = 'none';
    }

    function showUploadError(errors) {
        let html = '<strong>שגיאות באימות:</strong><ul>';
        errors.forEach(err => {
            html += `<li>${err}</li>`;
        });
        html += '</ul>';
        uploadError.innerHTML = html;
        uploadError.style.display = 'block';
    }

    function hideUploadError() {
        uploadError.style.display = 'none';
    }

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Collect form data
        const formDataObj = collectFormData();

        // Check if PDF is uploaded but not validated
        if (uploadedPdfFile && !pdfValidated) {
            showError('יש לאמת את קובץ ה-PDF לפני השליחה');
            return;
        }

        // Show loading spinner
        showLoading();
        hideError();

        try {
            let response;

            if (uploadedPdfFile && pdfValidated) {
                // Use uploaded PDF - send as multipart form data
                const formData = new FormData();
                formData.append('pdf_file', uploadedPdfFile);
                formData.append('form_data', JSON.stringify(formDataObj));

                response = await fetch('/api/fill-uploaded', {
                    method: 'POST',
                    body: formData
                });
            } else {
                // Use template PDF - send as JSON
                response = await fetch('/api/fill', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formDataObj)
                });
            }

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to generate PDF');
            }

            // Get the PDF blob
            const blob = await response.blob();

            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `visit_report_${getTimestamp()}.pdf`;
            document.body.appendChild(a);
            a.click();

            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            hideLoading();

            // Optional: Show success message
            showSuccess('PDF generated successfully!');

        } catch (error) {
            console.error('Error:', error);
            hideLoading();
            showError(error.message || 'An error occurred while generating the PDF');
        }
    });

    // Collect all form data
    function collectFormData() {
        const data = {};
        const formElements = form.elements;

        for (let element of formElements) {
            if (!element.name) continue;

            if (element.type === 'checkbox') {
                // Handle checkboxes
                if (element.name.includes('.')) {
                    // Nested field (e.g., treatment_types.elderly_issues)
                    const parts = element.name.split('.');
                    if (!data[parts[0]]) {
                        data[parts[0]] = {};
                    }
                    data[parts[0]][parts[1]] = element.checked;
                } else {
                    data[element.name] = element.checked;
                }
            } else if (element.type === 'radio') {
                // Handle radio buttons
                if (element.checked) {
                    data[element.name] = element.value;
                }
            } else if (element.tagName === 'TEXTAREA' || element.tagName === 'INPUT') {
                // Handle text inputs and textareas
                const value = element.value.trim();
                if (value) {
                    data[element.name] = value;
                }
            }
        }

        // Add signature data if present
        if (signatureCanvas && !isSignatureEmpty()) {
            data.signature_image = getSignatureDataUrl();
        }

        return data;
    }

    // Validation (optional - customize as needed)
    function validateForm(data) {
        // Add your validation logic here
        // Return true if valid, false otherwise
        return true;
    }

    // Get current timestamp for filename
    function getTimestamp() {
        const now = new Date();
        return now.getFullYear() +
            String(now.getMonth() + 1).padStart(2, '0') +
            String(now.getDate()).padStart(2, '0') + '_' +
            String(now.getHours()).padStart(2, '0') +
            String(now.getMinutes()).padStart(2, '0') +
            String(now.getSeconds()).padStart(2, '0');
    }

    // UI Helper functions
    function showLoading() {
        loadingDiv.style.display = 'flex';
    }

    function hideLoading() {
        loadingDiv.style.display = 'none';
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';

        // Auto-hide after 5 seconds
        setTimeout(() => {
            hideError();
        }, 5000);
    }

    function hideError() {
        errorDiv.style.display = 'none';
    }

    function showSuccess(message) {
        // You can implement a success message display
        // For now, just log to console
        console.log(message);
    }

    // Auto-save to localStorage (optional feature)
    function setupAutoSave() {
        const inputs = form.querySelectorAll('input, textarea');

        inputs.forEach(input => {
            // Load saved value
            const savedValue = localStorage.getItem(`form_${input.name}`);
            if (savedValue !== null) {
                if (input.type === 'checkbox') {
                    input.checked = savedValue === 'true';
                } else {
                    input.value = savedValue;
                }
            }

            // Save on change
            input.addEventListener('change', () => {
                if (input.type === 'checkbox') {
                    localStorage.setItem(`form_${input.name}`, input.checked);
                } else {
                    localStorage.setItem(`form_${input.name}`, input.value);
                }
            });
        });
    }

    // Clear localStorage on form reset
    form.addEventListener('reset', () => {
        if (confirm('האם אתה בטוח שברצונך לנקות את הטופס?')) {
            // Clear localStorage
            const inputs = form.querySelectorAll('input, textarea');
            inputs.forEach(input => {
                localStorage.removeItem(`form_${input.name}`);
            });

            // Reset upload state
            resetUploadState();
            if (pdfUpload) {
                pdfUpload.value = '';
            }

            // Clear signature pad
            if (signatureCanvas && signatureCtx) {
                clearSignature();
            }
        }
    });

    // Optional: Enable auto-save feature
    // Uncomment the line below to enable auto-save
    // setupAutoSave();
});
