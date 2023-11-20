document.addEventListener('DOMContentLoaded', function () {
    // 페이지가 로드되면 실행되는 코드

    // 대학 선택 시 호출되는 함수
    function updateSubDepartments(departmentId) {
        // 서버에 대학에 해당하는 전공 정보 요청
        fetch(`/api/populate_database/`)
            .then(response => response.json())
            .then(data => {
                // 선택한 대학에 해당하는 전공만 필터링
                const subDepartments = data.sub_departments.filter(sub => sub.department_id === parseInt(departmentId));

                // 하위 메뉴 업데이트
                const subDepartmentContainer = document.getElementById('subDepartmentContainer');
                subDepartmentContainer.innerHTML = '';  // 기존 내용 비우기

                subDepartments.forEach(subDepartment => {
                    const subDepartmentItem = document.createElement('a');
                    subDepartmentItem.href = '#';  // 이곳에 선택한 전공에 대한 추가적인 동작을 추가할 수 있습니다.
                    subDepartmentItem.textContent = subDepartment.name;
                    subDepartmentContainer.appendChild(subDepartmentItem);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    // 대학 선택 시 이벤트 리스너 등록
    const departmentButtons = document.querySelectorAll('.dropdown-item');
    departmentButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const selectedDepartmentId = this.getAttribute('data-department-id');
            updateSubDepartments(selectedDepartmentId);
        });
    });
});
