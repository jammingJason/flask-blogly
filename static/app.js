function checkBoxes(id) {
  cb = document.getElementById(id);
  cb.checked = true;
  alert(cb);
}

async function checkBoxes(tagID, postID) {
  cb = document.getElementById(tagID);
  if (cb.checked == true) {
    // alert('True');
    let response = await axios.get('/tags/' + tagID + '/add-to-post/' + postID);
  } else {
    // alert('False');
    let response = await axios.get(
      '/tags/' + tagID + '/remove-from-post/' + postID
    );
  }
  // let response = await axios.get('/');
  // console.log('got', response);
  // return response.data;
}

function submitForm(formID) {
  form = document.getElementById(formID);
  form.submit();
}
