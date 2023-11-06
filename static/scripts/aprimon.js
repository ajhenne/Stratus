// ADD ROW LISTENER
document.addEventListener('DOMContentLoaded', function () {

  const apriballNames = ['fast', 'lure', 'level', 'heavy', 'love', 'moon', 'dream', 'safari', 'beast', 'sport'];

  const addRowBtn = document.getElementById('add-aprimon-btn');
  const popup = document.getElementById('add-aprimon-popup');
  const addRowForm = document.getElementById('add-row-form');
  const searchGridContainer = document.getElementById('search-container');

  // Show form.
  addRowBtn.addEventListener('click', function () {
    popup.classList.remove('hidden');
  });

  // Input form listener.
  const fieldInput = document.getElementById('add-aprimon-input');
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
            // console.log('static/sprites/pokemon/' + result.internalId + '.png')

            const panel = document.createElement('div');
            panel.classList.add('panel');

            const image = document.createElement('img');
            image.src = 'static/sprites/pokemon/' + result.internalId + '.png';
            image.alt = String(result.internalId)
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

  // Highlight ball boxes.
  const ball_checkboxes = document.querySelectorAll('.form-apriball input[type="checkbox"]')

  ball_checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      const apriballType = this.getAttribute('apriball-type');
      const isChecked = this.checked;
      const imgElement = document.getElementById(`apriball-image-${apriballType}`);
      const labelElement = document.getElementById(`form-apriball-${apriballType}`);

      if (isChecked) {
        imgElement.classList.remove('greyscale');
        labelElement.classList.add('option_selected');
      } else {
        imgElement.classList.add('greyscale');
        labelElement.classList.remove('option_selected');
      }

      this.setAttribute('value', isChecked.toString());
    });
  });


  // Submission.
  addRowForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    // Create an array to store checkbox values in the same order as apriballNames
    const apriballTypes = apriballNames.map(apriballName => {
        const checkboxValue = formData.get(`checkbox-${apriballName}`) === 'true';
        return checkboxValue;
    });

    // Now apriballTypes is guaranteed to be a list with true or false values based on the checkboxes' states
    const data = {
        pokemonName: formData.get('add-aprimon-input'),
        apriballTypes: apriballTypes
    };  

    fetch('/add_aprimon', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          location.reload()
        } else {
          alert('Failed to add a new row.');
        }
      })
      .catch(error => console.error('Error:', error))
  });

});