// ADD ROW LISTENER
document.addEventListener('DOMContentLoaded', function () {
  
  // FORM POPUP =======================================================================================================
  
  const addRowBtn = document.getElementById('add-aprimon-btn');
  const popup = document.getElementById('add-aprimon-popup');
  
  addRowBtn.addEventListener('click', function () {
    popup.classList.remove('hidden');
  });
  
  // SEARCH HANDLER ===================================================================================================
  
  const fieldInput = document.getElementById('add-aprimon-input');
  const searchGridContainer = document.getElementById('search-container');

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

            const panel = document.createElement('label');
            panel.classList.add('add-aprimon-search-panel');
            
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = 'aprimon-search-selection';
            radio.value = result.internalId;
            radio.classList.add('add-aprimon-radio')
            panel.appendChild(radio);

            const image = document.createElement('img');
            image.src = 'static/sprites/pokemon/' + result.internalId + '.png';
            image.alt = String(result.internalId)
            panel.appendChild(image)

            const text = document.createElement('div');
            text.classList.add('panel-text');
            text.textContent = result.name
            panel.appendChild(text)
            
            panel.addEventListener('click', () => {
              let radioButtons = document.querySelectorAll('.add-aprimon-search-panel');
              radioButtons.forEach(function(l) {
                l.classList.remove('option_selected');
              });
              panel.classList.add('option_selected');
            });
            // Listener to send selection to hidden submission form element.
            radio.addEventListener('click', () => {
              document.getElementById('add-aprimon-selected').value = result.internalId
            });

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

  // POKEMON SELECTION HANDLER ========================================================================================

  // Just used to highlight the Pokemon selected. Was having a hard time doing this in pure CSS for some reason.
  const radioButtons = document.querySelectorAll('.add-aprimon-search-panel');

  radioButtons.forEach(function(radio_button) {
      radio_button.addEventListener('click', function() {
          radioButtons.forEach(function(l) {
              l.classList.remove('option_selected');
          });
          this.classList.add('option_selected');
      });
  });
  // const searchResults = document.querySelectorAll('.add-aprimon-search-panel input[type="radio"]');
  // let selectedValue = null;

  // searchResults.forEach(searchResult => {
  //   searchResult.addEventListener('click', () => {
  //     console.log("YES")
  //     selectedValue = searchResult.id;
  //     searchResult.classList.add('option_selected')

  //   })
  // })



  // BALL SELECTION HANDLER ===========================================================================================

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

  // SUBMISSION =======================================================================================================

  const addRowForm = document.getElementById('add-row-form');
  const apriballNames = ['fast', 'lure', 'level', 'heavy', 'love', 'moon', 'dream', 'safari', 'beast', 'sport'];

  // Submission.
  addRowForm.addEventListener('submit', function (event) {
    event.preventDefault();

    // Guard clause to check a pokemon has been selected.
    let selectedValue = document.getElementById('add-aprimon-selected').value;
    if (selectedValue === '') {
      alert("Please first search for and select a valid Pokemon.")
      return;
    };

    const formData = new FormData(event.target);

    // Create an array to store checkbox values in the same order as apriballNames
    const apriballTypes = apriballNames.map(apriballName => {
        const checkboxValue = formData.get(`checkbox-${apriballName}`) === 'true';
        return checkboxValue;
    });

    // Now apriballTypes is guaranteed to be a list with true or false values based on the checkboxes' states
    const data = {
        selectedPokemon: selectedValue,
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
        } else if (data.status === 'already_exists') {
          alert('Pokemon already exists in database. Select a new one.')
        } else {
          alert(data.message);
        }
      })
      .catch(error => console.error('Error:', error))
  });

});