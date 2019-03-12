console.log('Client-side code running');

const button = document.getElementById('compileButton');
button.addEventListener('click', function(e) {
  console.log('button was clicked');

  fetch('/compile', {method: 'POST'})
  .then(function(response) {
    if(response.ok) {
      console.log('Click was recorded');
      return;
    }
    throw new Error('Request failed.');
  })
  .catch(function(error) {
    console.log(error);
  });
});