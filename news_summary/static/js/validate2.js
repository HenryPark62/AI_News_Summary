document.addEventListener('DOMContentLoaded', function () {
    const step2 = document.getElementById('step-2');
    const step3 = document.getElementById('step-3');
    const startButton = document.getElementById('start-button');

    const modelRadios = document.querySelectorAll('input[name="model"]');
    const styleRadios = document.querySelectorAll('input[name="style"]');
    const fileInput = document.querySelector('input[name="file"]');
    const textInput = document.querySelector('textarea[name="text_content"]');

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

    function checkInputProvided() {
        const fileProvided = fileInput.files.length > 0;
        const textProvided = textInput.value.trim().length > 0;

        if (fileProvided || textProvided) {
            startButton.disabled = false;   // 입력이 있으면 활성화
        } else {
            startButton.disabled = true;    // 입력 없으면 다시 비활성화
        }
    }

    // 단계 이동용
    modelRadios.forEach(radio => radio.addEventListener('change', handleStepProgression));
    styleRadios.forEach(radio => radio.addEventListener('change', handleStepProgression));

    // 입력 확인용
    fileInput.addEventListener('change', checkInputProvided);
    textInput.addEventListener('input', checkInputProvided);

    // 초기 상태에서도 입력 상태를 체크
    checkInputProvided();
});