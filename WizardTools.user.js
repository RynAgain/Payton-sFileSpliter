// ==UserScript==
// @name         Wizard Tools
// @namespace    https://github.com/RynAgain/Payton-sFileSpliter
// @version      2.0.0
// @description  A powerful suite of tools with modern draggable UI - File Chunker, Text Tools, and more!
// @author       RynAgian
// @match        *://*/*
// @grant        none
// @require      https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js
// @downloadURL  https://github.com/RynAgain/Payton-sFileSpliter/raw/refs/heads/master/WizardTools.user.js
// @updateURL    https://github.com/RynAgain/Payton-sFileSpliter/raw/refs/heads/master/WizardTools.user.js
// @supportURL   https://github.com/RynAgain/Payton-sFileSpliter/issues
// @homepageURL  https://github.com/RynAgain/Payton-sFileSpliter
// @run-at       document-end
// ==/UserScript==

(function() {
    'use strict';

    // Global variables
    let isDragging = false;
    let isResizing = false;
    let dragOffset = { x: 0, y: 0 };
    let resizeStart = { x: 0, y: 0, width: 0, height: 0 };
    let currentTool = 'fileChunker';

    // Create the main wizard tools interface
    function createWizardToolsUI() {
        // Check if already exists
        if (document.getElementById('wizardToolsContainer')) {
            return;
        }

        // Create main container
        const container = document.createElement('div');
        container.id = 'wizardToolsContainer';
        container.innerHTML = `
            <div id="wizardToolsWindow" class="wizard-window">
                <div class="wizard-header" id="wizardHeader">
                    <div class="wizard-title">
                        <span class="wizard-icon">🧙‍♂️</span>
                        Wizard Tools
                    </div>
                    <div class="wizard-controls">
                        <button class="wizard-btn minimize" title="Minimize">−</button>
                        <button class="wizard-btn maximize" title="Maximize">□</button>
                        <button class="wizard-btn close" title="Close">×</button>
                    </div>
                </div>
                
                <div class="wizard-tabs">
                    <button class="tab-btn active" data-tool="fileChunker">📁 File Chunker</button>
                    <button class="tab-btn" data-tool="textTools">📝 Text Tools</button>
                    <button class="tab-btn" data-tool="colorPicker">🎨 Color Picker</button>
                    <button class="tab-btn" data-tool="calculator">🧮 Calculator</button>
                </div>
                
                <div class="wizard-content">
                    <!-- File Chunker Tool -->
                    <div id="fileChunker" class="tool-section active">
                        <h3>📁 File Chunker</h3>
                        <p>Split large CSV files into smaller chunks</p>
                        
                        <div class="form-group">
                            <label for="wizardFileInput">Select CSV File:</label>
                            <input type="file" id="wizardFileInput" accept=".csv" class="file-input">
                        </div>
                        
                        <div class="form-group">
                            <label for="wizardRowsPerChunk">Rows Per File:</label>
                            <input type="number" id="wizardRowsPerChunk" value="1000" min="1" class="number-input">
                        </div>
                        
                        <div class="form-group checkbox-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="wizardUploadValidation" checked>
                                <span class="checkmark"></span>
                                Upload Validation
                            </label>
                        </div>
                        
                        <button id="wizardChunkButton" class="action-btn">
                            <span class="btn-icon">⚡</span>
                            Chunk File & Download Zip
                        </button>
                        
                        <div id="wizardMessage" class="message"></div>
                    </div>

                    <!-- Text Tools -->
                    <div id="textTools" class="tool-section">
                        <h3>📝 Text Tools</h3>
                        <p>Various text manipulation utilities</p>
                        
                        <div class="form-group">
                            <label for="textInput">Input Text:</label>
                            <textarea id="textInput" class="text-area" placeholder="Enter your text here..."></textarea>
                        </div>
                        
                        <div class="button-grid">
                            <button class="tool-btn" onclick="transformText('upper')">UPPERCASE</button>
                            <button class="tool-btn" onclick="transformText('lower')">lowercase</button>
                            <button class="tool-btn" onclick="transformText('title')">Title Case</button>
                            <button class="tool-btn" onclick="transformText('reverse')">esreveR</button>
                            <button class="tool-btn" onclick="transformText('count')">Count Words</button>
                            <button class="tool-btn" onclick="transformText('clean')">Clean Spaces</button>
                        </div>
                        
                        <div class="form-group">
                            <label for="textOutput">Output:</label>
                            <textarea id="textOutput" class="text-area" readonly></textarea>
                        </div>
                    </div>

                    <!-- Color Picker -->
                    <div id="colorPicker" class="tool-section">
                        <h3>🎨 Color Picker</h3>
                        <p>Pick and convert colors between formats</p>
                        
                        <div class="form-group">
                            <label for="colorInput">Pick Color:</label>
                            <input type="color" id="colorInput" class="color-input" value="#667eea">
                        </div>
                        
                        <div class="color-info">
                            <div class="color-preview" id="colorPreview"></div>
                            <div class="color-values">
                                <div class="color-value">
                                    <label>HEX:</label>
                                    <input type="text" id="hexValue" readonly class="color-text">
                                </div>
                                <div class="color-value">
                                    <label>RGB:</label>
                                    <input type="text" id="rgbValue" readonly class="color-text">
                                </div>
                                <div class="color-value">
                                    <label>HSL:</label>
                                    <input type="text" id="hslValue" readonly class="color-text">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Calculator -->
                    <div id="calculator" class="tool-section">
                        <h3>🧮 Calculator</h3>
                        <p>Simple calculator with history</p>
                        
                        <div class="calc-display">
                            <input type="text" id="calcDisplay" readonly class="calc-input">
                        </div>
                        
                        <div class="calc-buttons">
                            <button class="calc-btn clear" onclick="clearCalc()">C</button>
                            <button class="calc-btn" onclick="calcInput('/')">/</button>
                            <button class="calc-btn" onclick="calcInput('*')">×</button>
                            <button class="calc-btn" onclick="deleteLast()">⌫</button>
                            
                            <button class="calc-btn" onclick="calcInput('7')">7</button>
                            <button class="calc-btn" onclick="calcInput('8')">8</button>
                            <button class="calc-btn" onclick="calcInput('9')">9</button>
                            <button class="calc-btn" onclick="calcInput('-')">-</button>
                            
                            <button class="calc-btn" onclick="calcInput('4')">4</button>
                            <button class="calc-btn" onclick="calcInput('5')">5</button>
                            <button class="calc-btn" onclick="calcInput('6')">6</button>
                            <button class="calc-btn" onclick="calcInput('+')">+</button>
                            
                            <button class="calc-btn" onclick="calcInput('1')">1</button>
                            <button class="calc-btn" onclick="calcInput('2')">2</button>
                            <button class="calc-btn" onclick="calcInput('3')">3</button>
                            <button class="calc-btn equals" onclick="calculate()" rowspan="2">=</button>
                            
                            <button class="calc-btn zero" onclick="calcInput('0')">0</button>
                            <button class="calc-btn" onclick="calcInput('.')">.</button>
                        </div>
                    </div>
                </div>
                <div class="wizard-resize-handle" id="resizeHandle"></div>
            </div>
        `;

        // Add comprehensive CSS styles
        const styles = `
            <style id="wizardToolsStyles">
                #wizardToolsContainer {
                    position: fixed;
                    top: 50px;
                    right: 50px;
                    z-index: 999999;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    font-size: 14px;
                    line-height: 1.4;
                }

                .wizard-window {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 12px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                    width: 450px;
                    min-width: 350px;
                    min-height: 250px;
                    max-width: 900px;
                    max-height: 700px;
                    overflow: hidden;
                    position: relative;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    transition: all 0.3s ease;
                }

                .wizard-header {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 12px 16px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    cursor: move;
                    user-select: none;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }

                .wizard-title {
                    color: white;
                    font-weight: 600;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }

                .wizard-icon {
                    font-size: 18px;
                }

                .wizard-controls {
                    display: flex;
                    gap: 4px;
                }

                .wizard-btn {
                    background: rgba(255, 255, 255, 0.2);
                    border: none;
                    color: white;
                    width: 24px;
                    height: 24px;
                    border-radius: 4px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 14px;
                    font-weight: bold;
                    transition: background 0.2s;
                }

                .wizard-btn:hover {
                    background: rgba(255, 255, 255, 0.3);
                }

                .wizard-btn.close:hover {
                    background: #ff4757;
                }

                .wizard-tabs {
                    background: rgba(255, 255, 255, 0.05);
                    display: flex;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }

                .tab-btn {
                    background: none;
                    border: none;
                    color: rgba(255, 255, 255, 0.7);
                    padding: 10px 15px;
                    cursor: pointer;
                    font-size: 12px;
                    transition: all 0.2s;
                    flex: 1;
                }

                .tab-btn:hover {
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                }

                .tab-btn.active {
                    background: rgba(255, 255, 255, 0.15);
                    color: white;
                    border-bottom: 2px solid white;
                }

                .wizard-content {
                    background: white;
                    padding: 20px;
                    max-height: 500px;
                    overflow-y: auto;
                }

                .tool-section {
                    display: none;
                }

                .tool-section.active {
                    display: block;
                }

                .tool-section h3 {
                    margin: 0 0 8px 0;
                    color: #333;
                    font-size: 18px;
                }

                .tool-section p {
                    margin: 0 0 20px 0;
                    color: #666;
                    font-size: 13px;
                }

                .form-group {
                    margin-bottom: 16px;
                }

                .form-group label {
                    display: block;
                    margin-bottom: 6px;
                    color: #333;
                    font-weight: 500;
                }

                .file-input, .number-input, .text-area, .color-text {
                    width: 100%;
                    padding: 10px 12px;
                    border: 2px solid #e1e8ed;
                    border-radius: 8px;
                    font-size: 14px;
                    transition: border-color 0.2s;
                    box-sizing: border-box;
                }

                .text-area {
                    min-height: 80px;
                    resize: vertical;
                    font-family: monospace;
                }

                .file-input:focus, .number-input:focus, .text-area:focus {
                    outline: none;
                    border-color: #667eea;
                }

                .checkbox-group {
                    display: flex;
                    align-items: center;
                }

                .checkbox-label {
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                    margin-bottom: 0 !important;
                }

                .checkbox-label input[type="checkbox"] {
                    display: none;
                }

                .checkmark {
                    width: 18px;
                    height: 18px;
                    border: 2px solid #e1e8ed;
                    border-radius: 4px;
                    margin-right: 8px;
                    position: relative;
                    transition: all 0.2s;
                }

                .checkbox-label input[type="checkbox"]:checked + .checkmark {
                    background: #667eea;
                    border-color: #667eea;
                }

                .checkbox-label input[type="checkbox"]:checked + .checkmark::after {
                    content: '✓';
                    position: absolute;
                    color: white;
                    font-size: 12px;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                }

                .action-btn, .tool-btn {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 12px 16px;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                    transition: transform 0.2s, box-shadow 0.2s;
                }

                .action-btn {
                    width: 100%;
                }

                .tool-btn {
                    padding: 8px 12px;
                    font-size: 12px;
                }

                .action-btn:hover, .tool-btn:hover {
                    transform: translateY(-1px);
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                }

                .action-btn:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                    transform: none;
                }

                .button-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 8px;
                    margin-bottom: 16px;
                }

                .color-input {
                    width: 100%;
                    height: 50px;
                    border: 2px solid #e1e8ed;
                    border-radius: 8px;
                    cursor: pointer;
                }

                .color-info {
                    display: flex;
                    gap: 16px;
                    align-items: center;
                }

                .color-preview {
                    width: 60px;
                    height: 60px;
                    border-radius: 8px;
                    border: 2px solid #e1e8ed;
                }

                .color-values {
                    flex: 1;
                }

                .color-value {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    margin-bottom: 8px;
                }

                .color-value label {
                    width: 40px;
                    margin: 0;
                    font-size: 12px;
                }

                .color-text {
                    flex: 1;
                    padding: 6px 8px;
                    font-size: 12px;
                    font-family: monospace;
                }

                .calc-display {
                    margin-bottom: 16px;
                }

                .calc-input {
                    width: 100%;
                    padding: 15px;
                    font-size: 18px;
                    text-align: right;
                    border: 2px solid #e1e8ed;
                    border-radius: 8px;
                    font-family: monospace;
                    background: #f8f9fa;
                }

                .calc-buttons {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 8px;
                }

                .calc-btn {
                    padding: 15px;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    background: #f8f9fa;
                    border: 2px solid #e1e8ed;
                    transition: all 0.2s;
                }

                .calc-btn:hover {
                    background: #e9ecef;
                    transform: translateY(-1px);
                }

                .calc-btn.clear {
                    background: #ff4757;
                    color: white;
                }

                .calc-btn.equals {
                    background: #667eea;
                    color: white;
                    grid-row: span 2;
                }

                .calc-btn.zero {
                    grid-column: span 2;
                }

                .message {
                    margin-top: 12px;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-size: 13px;
                    text-align: center;
                    min-height: 20px;
                }

                .message.success {
                    background: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                }

                .message.error {
                    background: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }

                .message.processing {
                    background: #d1ecf1;
                    color: #0c5460;
                    border: 1px solid #bee5eb;
                }

                .wizard-resize-handle {
                    position: absolute;
                    bottom: 0;
                    right: 0;
                    width: 16px;
                    height: 16px;
                    cursor: nw-resize;
                    background: linear-gradient(-45deg, transparent 0%, transparent 40%, rgba(255,255,255,0.3) 50%, transparent 60%, transparent 100%);
                }

                .wizard-window.minimized .wizard-content,
                .wizard-window.minimized .wizard-tabs,
                .wizard-window.minimized .wizard-resize-handle {
                    display: none;
                }

                .wizard-window.maximized {
                    width: 90vw !important;
                    height: 90vh !important;
                    top: 5vh !important;
                    left: 5vw !important;
                }

                #wizardToggleBtn {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    width: 56px;
                    height: 56px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    border-radius: 50%;
                    color: white;
                    font-size: 24px;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                    z-index: 999998;
                    transition: transform 0.2s, box-shadow 0.2s;
                }

                #wizardToggleBtn:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
                }

                .hidden {
                    display: none !important;
                }
            </style>
        `;

        // Add styles to head
        document.head.insertAdjacentHTML('beforeend', styles);

        // Add container to body
        document.body.appendChild(container);

        // Initialize functionality
        initializeDragAndResize();
        initializeFileChunker();
        initializeControls();
        initializeTabs();
        initializeTextTools();
        initializeColorPicker();
        initializeCalculator();
    }

    // Fixed drag and resize functionality
    function initializeDragAndResize() {
        const wizardWindow = document.getElementById('wizardToolsWindow');
        const header = document.getElementById('wizardHeader');
        const resizeHandle = document.getElementById('resizeHandle');
        const container = document.getElementById('wizardToolsContainer');

        // Drag functionality with proper event handling
        header.addEventListener('mousedown', startDrag);

        function startDrag(e) {
            if (e.target.closest('.wizard-controls')) return;
            
            isDragging = true;
            const rect = container.getBoundingClientRect();
            dragOffset.x = e.clientX - rect.left;
            dragOffset.y = e.clientY - rect.top;
            
            document.addEventListener('mousemove', handleDrag);
            document.addEventListener('mouseup', stopDrag);
            e.preventDefault();
            e.stopPropagation();
        }

        function handleDrag(e) {
            if (!isDragging) return;
            
            const newX = e.clientX - dragOffset.x;
            const newY = e.clientY - dragOffset.y;
            
            // Keep window within viewport bounds
            const maxX = window.innerWidth - 300;
            const maxY = window.innerHeight - 100;
            
            container.style.left = Math.max(0, Math.min(maxX, newX)) + 'px';
            container.style.top = Math.max(0, Math.min(maxY, newY)) + 'px';
            container.style.right = 'auto';
            container.style.bottom = 'auto';
        }

        function stopDrag() {
            isDragging = false;
            document.removeEventListener('mousemove', handleDrag);
            document.removeEventListener('mouseup', stopDrag);
        }

        // Resize functionality
        resizeHandle.addEventListener('mousedown', startResize);

        function startResize(e) {
            isResizing = true;
            const rect = wizardWindow.getBoundingClientRect();
            resizeStart.x = e.clientX;
            resizeStart.y = e.clientY;
            resizeStart.width = rect.width;
            resizeStart.height = rect.height;
            
            document.addEventListener('mousemove', handleResize);
            document.addEventListener('mouseup', stopResize);
            e.preventDefault();
            e.stopPropagation();
        }

        function handleResize(e) {
            if (!isResizing) return;
            
            const deltaX = e.clientX - resizeStart.x;
            const deltaY = e.clientY - resizeStart.y;
            const newWidth = Math.max(350, Math.min(900, resizeStart.width + deltaX));
            const newHeight = Math.max(250, Math.min(700, resizeStart.height + deltaY));
            
            wizardWindow.style.width = newWidth + 'px';
            wizardWindow.style.height = newHeight + 'px';
        }

        function stopResize() {
            isResizing = false;
            document.removeEventListener('mousemove', handleResize);
            document.removeEventListener('mouseup', stopResize);
        }
    }

    // Initialize window controls
    function initializeControls() {
        const wizardWindow = document.getElementById('wizardToolsWindow');
        const container = document.getElementById('wizardToolsContainer');
        const minimizeBtn = wizardWindow.querySelector('.minimize');
        const maximizeBtn = wizardWindow.querySelector('.maximize');
        const closeBtn = wizardWindow.querySelector('.close');

        minimizeBtn.addEventListener('click', () => {
            wizardWindow.classList.toggle('minimized');
            minimizeBtn.textContent = wizardWindow.classList.contains('minimized') ? '+' : '−';
        });

        maximizeBtn.addEventListener('click', () => {
            wizardWindow.classList.toggle('maximized');
            maximizeBtn.textContent = wizardWindow.classList.contains('maximized') ? '❐' : '□';
        });

        closeBtn.addEventListener('click', () => {
            container.classList.add('hidden');
            showToggleButton();
        });
    }

    // Initialize tabs
    function initializeTabs() {
        const tabBtns = document.querySelectorAll('.tab-btn');
        const toolSections = document.querySelectorAll('.tool-section');

        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const tool = btn.dataset.tool;
                
                // Update active tab
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Update active tool section
                toolSections.forEach(section => section.classList.remove('active'));
                document.getElementById(tool).classList.add('active');
                
                currentTool = tool;
            });
        });
    }

    // Initialize file chunker functionality (same as before)
    function initializeFileChunker() {
        const chunkButton = document.getElementById('wizardChunkButton');
        const messageEl = document.getElementById('wizardMessage');

        function updateMessage(text, type = '') {
            messageEl.textContent = text;
            messageEl.className = 'message ' + type;
        }

        chunkButton.addEventListener('click', function() {
            const fileInput = document.getElementById('wizardFileInput');
            if (fileInput.files.length === 0) {
                updateMessage('Please select a CSV file to upload.', 'error');
                return;
            }

            const file = fileInput.files[0];
            const rowsPerFile = parseInt(document.getElementById('wizardRowsPerChunk').value, 10);
            if (isNaN(rowsPerFile) || rowsPerFile < 1) {
                updateMessage('Please enter a valid number of rows per file.', 'error');
                return;
            }

            chunkButton.disabled = true;
            updateMessage('Processing...', 'processing');

            if (typeof JSZip === 'undefined') {
                updateMessage('JSZip library is required for zipping the files.', 'error');
                chunkButton.disabled = false;
                return;
            }

            const reader = new FileReader();
            reader.onload = function(event) {
                try {
                    const csvData = event.target.result;
                    const expectedHeader = "Store - 3 Letter Code,Item Name,Item PLU/UPC,Availability,Current Inventory,Sales Floor Capacity,Andon Cord,Tracking Start Date,Tracking End Date";
                    const doValidation = document.getElementById('wizardUploadValidation').checked;

                    function customParseCSV(data) {
                        const lines = data.split('\n');
                        const parsedData = [];
                        const expectedColumns = 9;

                        lines.forEach(line => {
                            let fields = line.split(',');
                            for (let i = 0; i < fields.length - 1; i++) {
                                if (fields[i].endsWith(',') && fields[i + 1].startsWith(' ')) {
                                    fields[i] = fields[i] + fields[i + 1];
                                    fields.splice(i + 1, 1);
                                }
                            }
                            while (fields.length < expectedColumns) {
                                fields.push('');
                            }
                            parsedData.push(fields);
                        });

                        return parsedData;
                    }

                    const parsedData = customParseCSV(csvData);
                    if (parsedData.length === 0) {
                        updateMessage('CSV file is empty.', 'error');
                        chunkButton.disabled = false;
                        return;
                    }

                    const header = parsedData[0].join(',');
                    if (doValidation && header.trim() !== expectedHeader.trim()) {
                        updateMessage("CSV header does not match expected format.", 'error');
                        chunkButton.disabled = false;
                        return;
                    }

                    const dataRows = [];
                    for (let i = 1; i < parsedData.length; i++) {
                        const isBlank = parsedData[i].every(field => field.trim() === "");
                        const joined = parsedData[i].join(',').replace(/[\s,]/g, "");
                        if (!isBlank && joined.length > 0) {
                            dataRows.push(parsedData[i].join(','));
                        }
                    }

                    const totalChunks = Math.ceil(dataRows.length / rowsPerFile);
                    const zip = new JSZip();
                    
                    for (let i = 0; i < totalChunks; i++) {
                        const chunkData = dataRows.slice(i * rowsPerFile, (i + 1) * rowsPerFile);
                        const chunkCsv = [header].concat(chunkData).join('\n');
                        zip.file('chunk_' + (i + 1) + '.csv', chunkCsv);
                    }

                    zip.generateAsync({ type: 'blob' }).then(function(content) {
                        const link = document.createElement('a');
                        link.href = window.URL.createObjectURL(content);
                        link.download = 'chunked_files.zip';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        updateMessage(`Success: ${totalChunks} files chunked and zip downloaded.`, 'success');
                        chunkButton.disabled = false;
                    }).catch(function(error) {
                        console.error('Error generating zip file:', error);
                        updateMessage('An error occurred while generating the zip file.', 'error');
                        chunkButton.disabled = false;
                    });
                } catch (err) {
                    console.error('Error processing CSV:', err);
                    updateMessage('An error occurred: ' + err.message, 'error');
                    chunkButton.disabled = false;
                }
            };
            reader.readAsText(file);
        });
    }

    // Initialize text tools
    function initializeTextTools() {
        window.transformText = function(action) {
            const input = document.getElementById('textInput').value;
            const output = document.getElementById('textOutput');
            
            switch(action) {
                case 'upper':
                    output.value = input.toUpperCase();
                    break;
                case 'lower':
                    output.value = input.toLowerCase();
                    break;
                case 'title':
                    output.value = input.replace(/\w\S*/g, (txt) =>
                        txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
                    break;
                case 'reverse':
                    output.value = input.split('').reverse().join('');
                    break;
                case 'count':
                    const words = input.trim().split(/\s+/).filter(word => word.length > 0);
                    const chars = input.length;
                    const lines = input.split('\n').length;
                    output.value = `Words: ${words.length}\nCharacters: ${chars}\nLines: ${lines}`;
                    break;
                case 'clean':
                    output.value = input.replace(/\s+/g, ' ').trim();
                    break;
            }
        };
    }

    // Initialize color picker
    function initializeColorPicker() {
        const colorInput = document.getElementById('colorInput');
        const colorPreview = document.getElementById('colorPreview');
        const hexValue = document.getElementById('hexValue');
        const rgbValue = document.getElementById('rgbValue');
        const hslValue = document.getElementById('hslValue');

        function updateColorValues(hex) {
            colorPreview.style.backgroundColor = hex;
            hexValue.value = hex;
            
            // Convert hex to RGB
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            rgbValue.value = `rgb(${r}, ${g}, ${b})`;
            
            // Convert RGB to HSL
            const rNorm = r / 255;
            const gNorm = g / 255;
            const bNorm = b / 255;
            
            const max = Math.max(rNorm, gNorm, bNorm);
            const min = Math.min(rNorm, gNorm, bNorm);
            const diff = max - min;
            
            let h = 0;
            let s = 0;
            const l = (max + min) / 2;
            
            if (diff !== 0) {
                s = l > 0.5 ? diff / (2 - max - min) : diff / (max + min);
                
                switch (max) {
                    case rNorm:
                        h = ((gNorm - bNorm) / diff + (gNorm < bNorm ? 6 : 0)) / 6;
                        break;
                    case gNorm:
                        h = ((bNorm - rNorm) / diff + 2) / 6;
                        break;
                    case bNorm:
                        h = ((rNorm - gNorm) / diff + 4) / 6;
                        break;
                }
            }
            
            hslValue.value = `hsl(${Math.round(h * 360)}, ${Math.round(s * 100)}%, ${Math.round(l * 100)}%)`;
        }

        colorInput.addEventListener('input', (e) => {
            updateColorValues(e.target.value);
        });

        // Initialize with default color
        updateColorValues(colorInput.value);
    }

    // Initialize calculator
    function initializeCalculator() {
        let currentInput = '';
        let operator = '';
        let previousInput = '';
        
        const display = document.getElementById('calcDisplay');

        window.calcInput = function(value) {
            if (['+', '-', '*', '/'].includes(value)) {
                if (currentInput && !operator) {
                    operator = value;
                    previousInput = currentInput;
                    currentInput = '';
                    display.value = previousInput + ' ' + value + ' ';
                }
            } else {
                currentInput += value;
                if (operator) {
                    display.value = previousInput + ' ' + operator + ' ' + currentInput;
                } else {
                    display.value = currentInput;
                }
            }
        };

        window.calculate = function() {
            if (previousInput && operator && currentInput) {
                const prev = parseFloat(previousInput);
                const curr = parseFloat(currentInput);
                let result = 0;

                switch (operator) {
                    case '+':
                        result = prev + curr;
                        break;
                    case '-':
                        result = prev - curr;
                        break;
                    case '*':
                        result = prev * curr;
                        break;
                    case '/':
                        result = curr !== 0 ? prev / curr : 'Error';
                        break;
                }

                display.value = result;
                currentInput = result.toString();
                operator = '';
                previousInput = '';
            }
        };

        window.clearCalc = function() {
            currentInput = '';
            operator = '';
            previousInput = '';
            display.value = '';
        };

        window.deleteLast = function() {
            if (currentInput) {
                currentInput = currentInput.slice(0, -1);
                if (operator) {
                    display.value = previousInput + ' ' + operator + ' ' + currentInput;
                } else {
                    display.value = currentInput;
                }
            }
        };
    }

    // Show toggle button
    function showToggleButton() {
        if (document.getElementById('wizardToggleBtn')) return;

        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'wizardToggleBtn';
        toggleBtn.innerHTML = '🧙‍♂️';
        toggleBtn.title = 'Open Wizard Tools';
        
        toggleBtn.addEventListener('click', () => {
            document.getElementById('wizardToolsContainer').classList.remove('hidden');
            document.body.removeChild(toggleBtn);
        });

        document.body.appendChild(toggleBtn);
    }

    // Initialize the wizard tools
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', createWizardToolsUI);
        } else {
            createWizardToolsUI();
        }
    }

    // Start the script
    init();

})();