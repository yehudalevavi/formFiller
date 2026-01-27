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

    // Track uploaded file and validation state
    let uploadedPdfFile = null;
    let pdfValidated = false;

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
        }
    });

    // Optional: Enable auto-save feature
    // Uncomment the line below to enable auto-save
    // setupAutoSave();
});
