const like = document.getElementById('likeButton');

let url = 'like.php';

sendLike();
like.addEventListener('click', function () {
    sendLike(1);
});

async function sendLike(nb = 0) {
    axios.get(url, {
        params: {
            likes: nb
        }
    })
        .then(function (response) {
            console.log(response);
            document.getElementById('likeCount').innerText = response.data;
        })
        .catch(function (error) {
            console.log(error);
        })
}