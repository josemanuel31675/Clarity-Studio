document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const placeholderText = document.querySelector('.placeholder-text');
    const processBtn = document.getElementById('process-btn');
    const loader = document.getElementById('loader');
    const widthInput = document.getElementById('width-input');
    const heightInput = document.getElementById('height-input');
    
    let selectedFile = null;

    // Handle drag and drop
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('active');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('active');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('active');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file.');
            return;
        }
        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            // Once the preview image loads, we capture its natural dimensions
            imagePreview.onload = () => {
                widthInput.value = imagePreview.naturalWidth;
                heightInput.value = imagePreview.naturalHeight;
            };
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            placeholderText.style.display = 'none';
            processBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    processBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const width = widthInput.value;
        const height = heightInput.value;
        const removeBg = document.getElementById('remove-bg-checkbox').checked;

        const formData = new FormData();
        formData.append('image', selectedFile);
        if (width) formData.append('width', width);
        if (height) formData.append('height', height);
        formData.append('remove_bg', removeBg);

        // UI Feedback
        processBtn.disabled = true;
        loader.style.display = 'block';
        imagePreview.style.opacity = '0.3';

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'clarity_studio_logo.png';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                const error = await response.json();
                alert('Error: ' + error.error);
            }
        } catch (err) {
            console.error(err);
            alert('An error occurred while processing the image.');
        } finally {
            processBtn.disabled = false;
            loader.style.display = 'none';
            imagePreview.style.opacity = '1';
        }
    });
});
