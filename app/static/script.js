document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const dropZone = document.getElementById('drop-zone');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultSection = document.getElementById('result-section');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const resultBadge = document.getElementById('result-badge');
    const progBar = document.getElementById('prog-bar');
    const confidenceVal = document.getElementById('confidence-val');

    let selectedFile = null;

    // Trigger file input
    dropZone.addEventListener('click', () => {
        if (!selectedFile) fileInput.click();
    });

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    ['dragleave', 'drop'].forEach(event => {
        dropZone.addEventListener(event, () => {
            dropZone.classList.remove('drag-over');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length) handleFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload a valid X-ray image.');
            return;
        }

        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            analyzeBtn.classList.remove('disabled');
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        selectedFile = null;
        fileInput.value = '';
        previewContainer.classList.add('hidden');
        analyzeBtn.classList.add('disabled');
        analyzeBtn.disabled = true;
        resultSection.classList.add('hidden');
    });

    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // Reset UI
        resultSection.classList.remove('hidden');
        loader.classList.remove('hidden');
        resultContent.classList.add('hidden');
        progBar.style.width = '0%';

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                setTimeout(() => {
                    showResult(data.result, data.confidence);
                }, 1500); // Artificial delay for "AI thinking" experience
            } else {
                alert(data.error || 'Prediction failed');
                resultSection.classList.add('hidden');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Could not connect to the analysis server.');
            resultSection.classList.add('hidden');
        }
    });

    function showResult(result, confidence) {
        loader.classList.add('hidden');
        resultContent.classList.remove('hidden');

        resultBadge.textContent = result;
        resultBadge.className = 'result-badge ' + (result === 'Pneumonia' ? 'badge-pneumonia' : 'badge-normal');
        
        const confNum = parseFloat(confidence);
        confidenceVal.textContent = confidence;
        
        // Progress bar animation
        setTimeout(() => {
            progBar.style.width = confNum + '%';
        }, 100);
    }
});
