const exampleModal = document.getElementById('exampleModal')
if (exampleModal) {
  exampleModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const recipient = button.getAttribute('data-bs-charmid')
    // If necessary, you could initiate an Ajax request here
    // and then do the updating in a callback.

    // Update the modal's content.
    const modalTitle = exampleModal.querySelector('.modal-title')
    const modalBody = exampleModal.querySelector('.modal-body')
    const modalBodyInput = exampleModal.querySelector('.modal-body input')
    const modalLink = exampleModal.querySelector('#modal-link')
    console.log(modalLink)

    modalTitle.textContent = 'Confirm'
    modalBody.textContent = `Please confirm charm id ${recipient}`;
    //Tried to use Django links but apparently that is bad practice
    //https://stackoverflow.com/questions/37311042/call-django-urls-inside-javascript-on-click-event
    modalLink.setAttribute('href',`/biospecimen/charm_ids/${recipient}/`)
    console.log(modalLink)



  })
}

    //
    // const modalLink = exampleModal.getElementsByTagName('a')
  // modalLink.setAttribute('href',`/biospecimen/charm_ids/${recipient}/`)
  //modalLink.href = `{% url "biospecimen:list_of_bio_ids" ${recipient} %}`