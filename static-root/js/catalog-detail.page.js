function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const addToCart = () => {
    const cartAddEl = document.querySelectorAll(".addToCartBtn");

    cartAddEl.forEach(cartEl => {
        cartEl.addEventListener("click", (el) => {
            el.preventDefault();
            // console.log(el.target.href)
            const csrftoken = getCookie('csrftoken');
            fetch(`${el.target.href}`, {
                method: 'POST',
                credentials: "same-origin",
                headers: {'X-CSRFToken': csrftoken}
            }).then(r => {
                location.reload();
                el.target.parentElement.classList.toggle("active");
            });
        })
    })
}

function showMessage() {
    const messageDiv = document.querySelector('.abovebeyond');
    const addToFavorite = document.querySelector('.add-to-favorite');
    // addToFavorite.map(el => {
    //     el.addEventListener('click',)
    // })
    addToFavorite.addEventListener("click", (el) => {
        console.log("Click")
    })
}

showMessage();


// function showMessage(message) {
//     const messageDiv = document.querySelector('.abovebeyond');
//     console.log(message, messageDiv);
// }
//
addToCart();