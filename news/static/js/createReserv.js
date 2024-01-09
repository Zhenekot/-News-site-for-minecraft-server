document.addEventListener('DOMContentLoaded', function() {
    const numberPeopleField = document.querySelector('#id_number_of_people');
    const setPeopleButton = document.querySelector('button[name="set_people"]');
     function updateDeleteButtonsVisibility() {
        const deleteButtons = formsetContainer.querySelectorAll('.delete-button');
        if (deleteButtons.length === 1) {
            deleteButtons[0].style.display = 'none';
        } else {
            deleteButtons.forEach(button => button.style.display = 'inline-block');
        }
    }


    const formsetContainer = document.querySelector('.people-info');

    formsetContainer.addEventListener('click', function(event) {

         if (event.target.classList.contains('delete-button')) {
            event.preventDefault();
            const form = event.target.closest('.dynamic-form');
            form.remove();
            numberPeopleField.value = numberPeopleField.value - 1;
            setPeopleButton.click();
            updateDeleteButtonsVisibility();
        }
    });

     updateDeleteButtonsVisibility(); // Call this function initially to ensure correct state
});