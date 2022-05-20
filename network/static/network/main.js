function addNewPost() {
  document.getElementById('add_new_post').style.display = "block";
  document.getElementById('btn_add_new_post').style.display = "none";
}

function follow(user_id, x) {
  fetch('/follow/' + user_id, {
    method: 'PUT',
    body: JSON.stringify({
      [x]: user_id
    })
  })
    .then(response => response.json())
    .then(result => {
      document.querySelector('#num_followers').innerHTML = 'Followers: ' + result.followers_counter;
      console.log(result.message)
    });
}


function vote(elem, user_id, x) {
  let mId = elem.parentNode.id;
  fetch('/post/' + mId, {
    method: 'PUT',
    body: JSON.stringify({
      [x]: user_id
    })
  })
    .then(response => response.json())
    .then(result => {
      document.querySelector("#likes-counter-" + mId).innerHTML = result.likes_counter;
      console.log(result);
    });
}

function editPost(postId) {

  const pfo = document.createElement('Form');
  pfo.id = 'edit-post-form';
  pfo.className = 'form-group';
  let text = document.querySelector('#post' + postId + '-text').innerHTML;
  pfo.value = document.querySelector('#post' + postId + '-text').innerHTML;
  document.querySelector('#post' + postId + '-text').replaceWith(pfo);

  const mra = document.createElement('input');
  mra.id = 'edit-post-area';
  mra.className = "form-control"
  mra.value = text;

  const bth = document.createElement('Button');
  bth.id = "but-sub";
  bth.className = 'btn btn-primary';
  bth.type = "submit";
  bth.innerHTML = 'Save';
  document.querySelector('#edit-post-form').append(mra);
  document.querySelector('#edit-post-form').append(bth);
  document.querySelector('#but-sub').addEventListener('click', (event) => {

    let newtext = document.querySelector('#edit-post-area').value;
    console.log(newtext)

    fetch('/edit_post/' + postId, {
      method: 'PUT',
      body: JSON.stringify({
        'post': newtext
      })
    })
      .then(response => response.json())
      .then(result => {

        const sto = document.createElement('div');
        sto.id = 'post' + postId + '-text';
        sto.innerHTML = newtext;
        document.querySelector('#edit-post-form').replaceWith(sto);
        console.log(result);

      });
    event.preventDefault();
  });
}


