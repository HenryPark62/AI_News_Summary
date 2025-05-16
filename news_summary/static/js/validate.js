document.addEventListener('DOMContentLoaded', function () {
    const step2 = document.getElementById('step-2');
    const step3 = document.getElementById('step-3');
    const startButton = document.getElementById('start-button');

    const modelRadios = document.querySelectorAll('input[name="model"]');
    const styleRadios = document.querySelectorAll('input[name="style"]');
    const fileInput = document.querySelector('input[name="file"]');
    const textInput = document.querySelector('textarea[name="text_content"]');

    const fileNameDisplay = document.getElementById('file-name');
    const textCountDisplay = document.getElementById('text-count');

    // URL input 감지
    const urlInput = document.querySelector('input[name="news_url"]');
    const newsSourceRadios = document.querySelectorAll('input[name="news_source"]');

    let uploadedFileTextLength = 0;
    let fileUploaded = false; // 파일 업로드 여부
    let textEntered = false; // 텍스트 입력 여부

    function handleStepProgression() {
        const modelSelected = Array.from(modelRadios).some(radio => radio.checked);
        const styleSelected = Array.from(styleRadios).some(radio => radio.checked);

        if (modelSelected && step2.classList.contains('hidden')) {
            step2.classList.remove('hidden');
            setTimeout(() => step2.classList.add('show'), 50);
        }

        if (modelSelected && styleSelected && step3.classList.contains('hidden')) {
            step3.classList.remove('hidden');
            setTimeout(() => step3.classList.add('show'), 50);
        }
    }

    function updateTextCount() {
        const textLength = textInput.value.trim().length;
        const totalLength = textLength + uploadedFileTextLength;
        textCountDisplay.textContent = `${totalLength}자 입력됨`;
    }

    function checkInputProvided() {
        const fileProvided = fileInput.files.length > 0;
        const textProvided = textInput.value.trim().length > 0;
        const urlProvided = urlInput.value.trim().length > 0;
        const sourceSelected = Array.from(newsSourceRadios).some(radio => radio.checked);
    
        // 하나라도 입력되었으면 버튼 활성화
        if (
            (fileProvided || textProvided) || 
            (urlProvided && sourceSelected)
        ) {
            startButton.disabled = false;
        } else {
            startButton.disabled = true;
        }
    
        updateTextCount();
    }

    function resetFileUpload() {
        fileInput.value = "";
        fileNameDisplay.innerHTML = "";
        uploadedFileTextLength = 0;
        fileUploaded = false;
        updateTextCount();
        checkInputProvided();
    }

    function resetTextInput() {
        textInput.value = "";
        textEntered = false;
        updateTextCount();
        checkInputProvided();
    }

    // ⭐ 추가: 모델 선택 시
    modelRadios.forEach(radio => radio.addEventListener('change', () => {
        handleStepProgression();
    }));

    // ⭐ 추가: 스타일 선택 시
    styleRadios.forEach(radio => radio.addEventListener('change', () => {
        handleStepProgression();
    }));

    // 파일 업로드
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            if (textEntered) {
                alert("⚠️ 텍스트가 이미 입력되어 있습니다. 파일 입력을 초기화합니다.");
                resetFileUpload();
            }

            const file = fileInput.files[0];
            fileNameDisplay.innerHTML = "선택된 파일: " + file.name + " <span id='remove-file' style='cursor:pointer; color:red; margin-left:5px;'>❌</span>";
            fileUploaded = true;

            if (file.type === "text/plain") {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const content = e.target.result;
                    uploadedFileTextLength = content.trim().length;
                    updateTextCount();
                    checkInputProvided();
                    handleStepProgression(); 
                };
                reader.readAsText(file, 'utf-8');
            } else {
                alert("텍스트(.txt) 파일만 업로드할 수 있습니다.");
                resetFileUpload();
            }

            setTimeout(() => {
                const removeBtn = document.getElementById('remove-file');
                if (removeBtn) {
                    removeBtn.addEventListener('click', resetFileUpload);
                }
            }, 50);
        } else {
            resetFileUpload();
        }
    });

    // 텍스트 입력
    textInput.addEventListener('input', () => {
        if (fileUploaded) {
            alert("⚠️ 파일이 이미 업로드되어 있습니다. 텍스트를 초기화합니다.");
            resetTextInput(); // 나중에 텍스트 입력했으니 파일을 지운다
        }

        if (textInput.value.trim().length > 0) {
            textEntered = true;
        } else {
            textEntered = false;
        }

        updateTextCount();
        checkInputProvided();
        handleStepProgression(); 
    });

    // 뉴스 URL 입력
    urlInput.addEventListener('input', () => {
        checkInputProvided();
        handleStepProgression();
    });

    // 언론사 라디오 선택
    newsSourceRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            checkInputProvided();
            handleStepProgression();
        });
    });

    // 초기 상태 체크
    checkInputProvided();
});