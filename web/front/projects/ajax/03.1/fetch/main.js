const like = document.getElementById('likeButton');

let url = 'like.php';

sendLike();
like.addEventListener('click', function () {
  sendLike(1);
});

async function sendLike(nb = 0) {
  fetch((nb > 0) ? url + '?likes=' + nb : url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    },
  }).then(response => response.json())
    .then(data => {
      document.getElementById('likeCount').innerText = data;
    }).catch(function (error) {
      console.log(error);
    });
}