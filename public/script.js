document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-btn');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const emptyState = document.getElementById('empty-state');
    const resultBadge = document.getElementById('result-badge');
    const confidenceVal = document.getElementById('confidence-val');
    const circleStroke = document.getElementById('circle-stroke');
    const terminalFeed = document.getElementById('terminal-feed');
    const scanTime = document.getElementById('scan-time');
    const exampleItems = document.querySelectorAll('.example-item');

    let selectedFile = null;

    // Handle File Selection
    dropZone.addEventListener('click', () => {
        if (!selectedFile) fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });

    // Drag and Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });

    // Handle Example Clicks
    exampleItems.forEach(item => {
        item.addEventListener('click', async (e) => {
            const type = item.dataset.type;
            const imgPath = `assets/${type}.png`;
            
            try {
                const response = await fetch(imgPath);
                const blob = await response.blob();
                const file = new File([blob], `${type}_sample.png`, { type: 'image/png' });
                handleFile(file);
            } catch (err) {
                console.error('Failed to load example:', err);
            }
        });
    });

    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid medical radiographic image.');
            return;
        }

        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            analyzeBtn.classList.remove('disabled');
            analyzeBtn.disabled = false;
            resetUI();
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
        resetUI();
    });

    function resetUI() {
        emptyState.classList.remove('hidden');
        loader.classList.add('hidden');
        resultContent.classList.add('hidden');
        terminalFeed.innerHTML = '';
    }

    function updateTerminal(message) {
        const p = document.createElement('p');
        p.textContent = `> ${message}`;
        terminalFeed.appendChild(p);
        terminalFeed.scrollTop = terminalFeed.scrollHeight;
    }

    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        // UI State Transitions
        analyzeBtn.disabled = true;
        analyzeBtn.classList.add('disabled');
        emptyState.classList.add('hidden');
        resultContent.classList.add('hidden');
        loader.classList.remove('hidden');
        
        terminalFeed.innerHTML = '';
        const steps = [
            { msg: 'Connecting to Neural Engine...', delay: 800 },
            { msg: 'Layer 1: Edge detection active...', delay: 700 },
            { msg: 'Layer 4: Pattern normalization...', delay: 700 },
            { msg: 'Layer 12: Density variance check...', delay: 700 },
            { msg: 'Synthesizing diagnostic probability...', delay: 500 }
        ];

        try {
            // Start simulation steps
            for (const step of steps) {
                updateTerminal(step.msg);
                await new Promise(r => setTimeout(r, step.delay));
            }

            const formData = new FormData();
            formData.append('file', selectedFile);

            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                displayResult(data);
            } else {
                throw new Error(data.error || 'Prediction failed');
            }
        } catch (error) {
            console.error('Analysis failed:', error);
            updateTerminal('CRITICAL ERROR: Analysis sequence failed.');
            alert('Service temporary unavailable. Please try again.');
        } finally {
            loader.classList.add('hidden');
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('disabled');
        }
    });

    function displayResult(data) {
        resultContent.classList.remove('hidden');
        
        // Update Result Text & Badge
        const isPneumonia = data.result.toLowerCase() === 'pneumonia';
        resultBadge.textContent = isPneumonia ? 'Pneumonia Detected' : 'Normal / Healthy';
        resultBadge.className = `result-badge ${isPneumonia ? 'detected' : 'normal'}`;
        
        // Update Time
        const now = new Date();
        scanTime.textContent = `Scan ID: ${Math.random().toString(36).substr(2, 9).toUpperCase()} | ${now.toLocaleTimeString()}`;

        // Animate Percentage & Circle
        const percentage = parseFloat(data.confidence);
        animateValue('confidence-val', 0, percentage, 1000);
        
        // SVG circle stroke-dasharray animation
        circleStroke.style.strokeDasharray = `${percentage}, 100`;
        circleStroke.style.stroke = isPneumonia ? 'var(--accent)' : 'var(--success)';
    }

    function animateValue(id, start, end, duration) {
        const obj = document.getElementById(id);
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = start + (end - start) * progress;
            obj.innerHTML = current.toFixed(2) + '%';
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    }
});
