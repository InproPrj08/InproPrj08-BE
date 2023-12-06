let optionsButtons = document.querySelectorAll(".option-button");
let advancedOptionButton = document.querySelectorAll(".adv-option-button");
let fontName = document.getElementById("fontName");
let fontSizeRef = document.getElementById("fontSize");
let writingArea = document.getElementById("text-input");
let linkButton = document.getElementById("createLink");
let alignButtons = document.querySelectorAll(".align");
let spacingButtons = document.querySelectorAll(".spacing");
let formatButtons = document.querySelectorAll(".format");
let scriptButtons = document.querySelectorAll(".script");


let fontList = [
    "Arial",
    "Verdana",
    "Times New Roman",
    "Garamond",
    "Georgia",
    "Courier New",
    "Cursive",
];

const initializer = () => {
    highlighter(alignButtons, true);
    highlighter(spacingButtons, true);
    highlighter(formatButtons, false);
    highlighter(scriptButtons, true);

    fontList.map((value) => {
        let option = document.createElement("option");
        option.value = value;
        option.innerHTML = value;
        fontName.appendChild(option);
    });

    for (let i = 1; i <= 7; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.innerHTML = i;
        fontSizeRef.appendChild(option);
    }

    fontSizeRef.value = 3;
};

const modifyText = (command, defaultUi, value) => {
    document.execCommand(command, defaultUi, value);
};

optionsButtons.forEach((button) => {
    button.addEventListener("click", () => {
        modifyText(button.id, false, null);
    });
});

advancedOptionButton.forEach((button) => {
    button.addEventListener("change", () => {
        modifyText(button.id, false, button.value);
    });
});

linkButton.addEventListener("click", () => {
    let userLink = prompt("Enter a URL?");
    if (/http/i.test(userLink)) {
        modifyText(linkButton.id, false, userLink);
    } else {
        userLink = "http://" + userLink;
        modifyText(linkButton.id, false, userLink);
    }
});

const highlighter = (className, needsRemoval) => {
    className.forEach((button) => {
        button.addEventListener("click", () => {
            if (needsRemoval) {
                let alreadyActive = false;
                if (button.classList.contains("active")) {
                    alreadyActive = true;
                }
                highlighterRemover(className);
                if (!alreadyActive) {
                    button.classList.add("active");
                }
            } else {
                button.classList.toggle("active");
            }
        });
    });
};

const highlighterRemover = (className) => {
    className.forEach((button) => {
        button.classList.remove("active");
    });
};


function previewImage(input) {
        var imageContainer = document.getElementById('image-container');
        var imagePreview = document.getElementById('image-preview1');
        var imagePlaceholder = document.getElementById('image-preview-placeholder');
        var imageInput = input.files[0];

        if (!imageContainer) {
            // 이미지 컨테이너 엘리먼트가 생성되지 않은 경우
            imageContainer = document.createElement('div');
            imageContainer.id = 'image-container';
            document.body.appendChild(imageContainer);
        }

        if (!imagePreview) {
            // 이미지 미리보기 엘리먼트가 생성되지 않은 경우
            imagePreview = new Image();
            imagePreview.id = 'image-preview1';
            imagePreview.style.width = '150px';
            imagePreview.style.height = '200px';

            imageContainer.appendChild(imagePreview);
        }

        if (imageInput) {
            var reader = new FileReader();

            reader.onload = function (e) {
                // 이미지 미리보기 업데이트
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
                imagePlaceholder.style.display = 'none';
                imagePreview.style.borderRadius = '30px';

            };

            reader.readAsDataURL(imageInput);
        } else {
            console.error('No image input found.');
        }
    }

    // 프로필 사진 플레이스홀더를 클릭하면 이미지 입력란 열기
    function openImageInput() {
        document.getElementById('image-input').click();
    }

//편집기 이미지
const btnImage = document.getElementById('btn-image');
const imageSelector = document.getElementById('img-selector');

btnImage.addEventListener('click', function () {
    imageSelector.click();
});

imageSelector.addEventListener('change', function (e) {
    const files = e.target.files;
    if (!!files) {
        handleImage(files[0]);
    }
});

function focusEditor() {
    document.getElementById('text-input').focus();
}
function handleImage(file) {
    const reader = new FileReader();
    reader.addEventListener('load', function (e) {
        const imgElement = document.createElement('img');
        imgElement.src = reader.result;
        imgElement.setAttribute('class', 'resizable');
        document.getElementById('text-input').appendChild(imgElement);
        makeResizableDiv(imgElement);
    });

    // 이미지 크기 조절 및 추가 부분을 handleImage 함수 내에 직접 정의
    function resizeImage(file, maxWidth, maxHeight, callback) {
        const reader = new FileReader();

        reader.onload = function (event) {
            const img = new Image();
            img.src = event.target.result;

            img.onload = function () {
                let width = img.width;
                let height = img.height;

                if (width > maxWidth || height > maxHeight) {
                    const ratio = Math.min(maxWidth / width, maxHeight / height);

                    width *= ratio;
                    height *= ratio;
                }

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;

                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);

                canvas.toBlob(function (blob) {
                    callback(blob);
                }, file.type);
            };
        };

        reader.readAsDataURL(file);
    }

    // handleImage 함수 내에 resizeImage 함수 정의를 직접 포함
    resizeImage(file, 400, 300, function (resizedBlob) {
        reader.readAsDataURL(resizedBlob);
    });
}

        function makeResizableDiv(element) {
            const resizer = document.createElement('div');
            resizer.className = 'resizer';
            element.appendChild(resizer);

            let prevX = 0;
            let prevY = 0;
            let isResizing = false;

            resizer.addEventListener('mousedown', function (e) {
                prevX = e.clientX;
                prevY = e.clientY;
                isResizing = true;
            });

            document.addEventListener('mousemove', function (e) {
                if (isResizing) {
                    element.style.width = element.offsetWidth - (prevX - e.clientX) + 'px';
                    element.style.height = element.offsetHeight - (prevY - e.clientY) + 'px';
                    prevX = e.clientX;
                    prevY = e.clientY;
                }
            });

            document.addEventListener('mouseup', function () {
                isResizing = false;
            });
        }

        function resizeImage(file, maxWidth, maxHeight, callback) {
    const reader = new FileReader();

    reader.onload = function (event) {
        const img = new Image();
        img.src = event.target.result;

        img.onload = function () {
            let width = img.width;
            let height = img.height;

            if (width > maxWidth || height > maxHeight) {
                const ratio = Math.min(maxWidth / width, maxHeight / height);

                width *= ratio;
                height *= ratio;
            }

            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);  // 올바른 크기로 그림

            canvas.toBlob(function (blob) {
                callback(blob);
            }, file.type);
        };
    };

    reader.readAsDataURL(file);
}

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


window.onload = initializer;