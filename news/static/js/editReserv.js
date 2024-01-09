document.addEventListener('DOMContentLoaded', function() {
    var statusSelect = document.getElementById('id_status');
    var fullCostInput = document.getElementById('id_full_cost');

    function updateFullCostInput() {
        if (statusSelect.value === 'Подтвержден') {
            fullCostInput.removeAttribute('disabled');
        } else {
            fullCostInput.setAttribute('disabled', 'disabled');
            fullCostInput.value = '';
        }
    }

    statusSelect.addEventListener('change', updateFullCostInput);
    updateFullCostInput();
});