// ADD ROW LISTENER
document.addEventListener('DOMContentLoaded', function() {

  const addRowBtn = document.getElementById('add-aprimon-btn');
  const popup = document.getElementById('add-aprimon-popup');
  const addRowForm = document.getElementById('add-row-form');
  const searchGridContainer = document.getElementById('search-container');

  const fieldInput = document.getElementById('add-aprimon-input');

  // Show form.
  addRowBtn.addEventListener('click', function() {
    popup.classList.remove('hidden');
  });

  // Input form listener.
  fieldInput.addEventListener('input', searchName);

  function searchName() {
    const enteredName = fieldInput.value;

    searchGridContainer.innerHTML = ''

    fetch('/search_pokemon', {
      method: 'POST',
      body: JSON.stringify({ name: enteredName }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then(response => response.json())
    .then(data => {

      // Search success; display results.
      if (data.status === 'success') {
        searchGridContainer.innerHTML = ''
        data.results.forEach(result => {
          console.log('static/sprites/pokemon/' + result.internalId + '.png')

          const panel = document.createElement('div');
          panel.classList.add('panel');

          const image = document.createElement('img');
          image.src = 'static/sprites/pokemon/' + result.internalId + '.png';
          image.alt = 'image test'
          panel.appendChild(image)
          
          const text = document.createElement('div');
          text.classList.add('panel-text');
          text.textContent = result.name
          panel.appendChild(text)

          searchGridContainer.appendChild(panel);
        });

      // Nothing found.
      } else if (data.status === 'not_found') {
        searchGridContainer.innerHTML = ''
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  // Submission.
  addRowForm.addEventListener('submit', function(event) {
    event.preventDefault();

    fetch('/add_aprimon', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: fieldInput.value }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        location.reload()
      } else {
        alert('Failed to add a new row.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  })
});