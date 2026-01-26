// PDF Form Filler - Client-side JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pdfForm');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error-message');

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Collect form data
        const formData = collectFormData();

        // Validate required fields (optional - add your validation logic)
        // if (!validateForm(formData)) {
        //     showError('Please fill in all required fields');
        //     return;
        // }

        // Show loading spinner
        showLoading();
        hideError();

        try {
            // Send data to server
            const response = await fetch('/api/fill', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

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
        }
    });

    // Optional: Enable auto-save feature
    // Uncomment the line below to enable auto-save
    // setupAutoSave();
});
