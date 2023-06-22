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

const removeFromCart = () => {
    const cartRemoveEl = document.querySelectorAll(".trash");
    cartRemoveEl.forEach(cartEl => {
        cartEl.addEventListener("click", (el) => {
            el.preventDefault();
            el.stopPropagation();
            const csrftoken = getCookie('csrftoken');
            fetch(`${el.target.parentElement.href}`, {
                method: 'POST',
                credentials: "same-origin",
                headers: {'X-CSRFToken': csrftoken}
            }).then(r => {
            });
        })
    })
}

const removeFromCartIcon = () => {
    const cartRemoveEl = document.querySelectorAll(".basket__remove-icon");
    cartRemoveEl.forEach(cartEl => {
        cartEl.addEventListener("click", (el) => {
            el.preventDefault();
            el.stopPropagation();
            const csrftoken = getCookie('csrftoken');

            fetch(`${el.target.href}`, {
                method: 'DELETE',
                credentials: "same-origin",
                headers: {
                    'X-CSRFToken': csrftoken
                }
            }).then(res => {
                if (res.status === 204) {
                    location.reload();
                }
            }).catch(err => console.error(err));
        })
    })
}


const clearCart = () => {
    const cartRemoveEl = document.querySelectorAll(".basket__clear-btn");
    cartRemoveEl.forEach(cartEl => {
        cartEl.addEventListener("click", (el) => {
            el.preventDefault();
            el.stopPropagation();
            const csrftoken = getCookie('csrftoken');

            fetch(`${el.target.href}`, {
                method: 'DELETE',
                credentials: "same-origin",
                headers: {
                    'X-CSRFToken': csrftoken,
                }
            }).then(res => {
                if (res.status === 204) {
                    location.reload();
                }
            }).catch(err => console.error(err));
        })
    })
}

removeFromCart();
removeFromCartIcon();
clearCart();