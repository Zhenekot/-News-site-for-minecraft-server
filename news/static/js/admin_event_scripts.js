document.addEventListener('DOMContentLoaded', function() {
    const transportSelect = document.querySelector('#id_transport');
    const seatsInput = document.querySelector('#id_count_place');

    if (transportSelect && seatsInput) {
        transportSelect.addEventListener('change', function() {
            fetch(`/get-seats-count/${this.value}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        console.error('Error:', data.error);
                    } else {
                        seatsInput.value = data.count_seat;
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    }
});